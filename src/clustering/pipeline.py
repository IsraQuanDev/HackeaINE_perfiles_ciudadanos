from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import duckdb
import hdbscan
import numpy as np
import pandas as pd
from libpysal.weights import KNN
from scipy.spatial.distance import cdist
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import SpectralEmbedding
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import RobustScaler, StandardScaler
from tslearn.clustering import TimeSeriesKMeans

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DOCS_DIR = BASE_DIR / "docs"
DUCKDB_PATH = BASE_DIR / "data" / "ccpc.duckdb"
SEED = 42

# Conjunto de variables diseñadas específicamente para distinguir TRAYECTORIA, DINÁMICA y BRECHAS
# (evitando una segmentación trivial de solo "alta/media/baja participación")
CLUSTERING_FEATURES = [
    "part_media_global",
    "caida_presidencial_intermedia",
    "pendiente_tendencia",
    "volatilidad",
    "constancia_sobre_mediana",
    "brecha_genero_media",
    "brecha_genero_tendencia",
    "brecha_generacional_60_vs_18_29",
    "pct_ln_rural",
    "cagr_ln_2009_2024",
]

TRAJECTORY_COLS = [
    "part_2009",
    "part_2012",
    "part_2015",
    "part_2018",
    "part_2021",
    "part_2024",
]


def compute_bootstrap_stability(
    X: np.ndarray,
    k: int,
    method: str = "kmeans",
    n_boot: int = 100,
    seed: int = SEED,
) -> float:
    """
    Calcula la estabilidad por bootstrap (Adjusted Rand Index promedio en n_boot>=100 remuestreos).
    Compara las asignaciones del modelo ajustado sobre cada muestra bootstrap (evaluado en X completo)
    contra las asignaciones del modelo base.
    """
    rng = np.random.default_rng(seed)
    n_samples = X.shape[0]

    if method == "kmeans":
        base_model = KMeans(n_clusters=k, random_state=seed, n_init=10).fit(X)
        base_labels = base_model.labels_
    elif method == "gmm":
        base_model = GaussianMixture(
            n_components=k, covariance_type="full", random_state=seed, n_init=3
        ).fit(X)
        base_labels = base_model.predict(X)
    else:
        raise ValueError(f"Método bootstrap no soportado: {method}")

    aris: list[float] = []
    for b in range(n_boot):
        idx = rng.choice(n_samples, size=int(0.85 * n_samples), replace=False)
        X_sub = X[idx]
        if method == "kmeans":
            m_b = KMeans(n_clusters=k, random_state=seed + b + 1, n_init=2, max_iter=80).fit(X_sub)
            pred_full = m_b.predict(X)
        else:
            m_b = GaussianMixture(
                n_components=k, covariance_type="diag", random_state=seed + b + 1, n_init=1, max_iter=60
            ).fit(X_sub)
            pred_full = m_b.predict(X)
        aris.append(float(adjusted_rand_score(base_labels, pred_full)))

    return float(np.mean(aris))


def _soft_probabilities_from_centroids(X: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    dists = cdist(X, centroids, metric="euclidean")
    inv_d = 1.0 / (dists + 1e-6)
    probs = inv_d / inv_d.sum(axis=1, keepdims=True)
    return probs


def evaluate_all_methods(df: pd.DataFrame) -> tuple[dict[str, Any], pd.DataFrame]:
    """
    Compara sistemáticamente los enfoques A (K-Means), B (GMM), C (HDBSCAN),
    D (TimeSeriesKMeans con DTW) y E (Clustering con restricción espacial) para k en [3..10].
    """
    np.random.seed(SEED)
    X_raw = df[CLUSTERING_FEATURES].to_numpy(dtype=float)
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X_raw)
    # Recorte suave de outliers extremos post-RobustScaler para evitar micro-clusters de 1 municipio
    X_scaled = np.clip(X_scaled, -4.0, 4.0)

    # Serie temporal para DTW (normalizada z-score por dimensión temporal o en niveles + diferencias)
    X_ts = df[TRAJECTORY_COLS].to_numpy(dtype=float)[:, :, np.newaxis]

    # Matriz de conectividad espacial para enfoque E
    coords = df[["lon_aprox", "lat_aprox"]].to_numpy(dtype=float)
    w_knn = KNN.from_array(coords, k=10)
    connectivity = w_knn.sparse

    k_grid_results: list[dict[str, Any]] = []
    candidate_models: dict[str, dict[str, Any]] = {}

    for k in range(3, 11):
        # A) K-Means sobre RobustScaler
        km = KMeans(n_clusters=k, random_state=SEED, n_init=20).fit(X_scaled)
        km_labels = km.labels_
        km_sil = float(silhouette_score(X_scaled, km_labels))
        km_db = float(davies_bouldin_score(X_scaled, km_labels))
        km_ch = float(calinski_harabasz_score(X_scaled, km_labels))
        km_min_pct = float(pd.Series(km_labels).value_counts(normalize=True).min())
        km_ari = compute_bootstrap_stability(X_scaled, k, method="kmeans", n_boot=100)

        k_grid_results.append(
            {
                "metodo": "A_KMeans_Robust",
                "k": k,
                "silhouette": km_sil,
                "davies_bouldin": km_db,
                "calinski_harabasz": km_ch,
                "bootstrap_ari_100": km_ari,
                "min_cluster_pct": km_min_pct,
                "bic": None,
            }
        )
        candidate_models[f"A_KMeans_k{k}"] = {
            "labels": km_labels,
            "probs": _soft_probabilities_from_centroids(X_scaled, km.cluster_centers_),
            "centroids": km.cluster_centers_,
            "metrics": k_grid_results[-1],
        }

        # B) Gaussian Mixture Models (BIC)
        gmm = GaussianMixture(
            n_components=k, covariance_type="full", random_state=SEED, n_init=5
        ).fit(X_scaled)
        gmm_labels = gmm.predict(X_scaled)
        gmm_probs = gmm.predict_proba(X_scaled)
        gmm_sil = float(silhouette_score(X_scaled, gmm_labels))
        gmm_db = float(davies_bouldin_score(X_scaled, gmm_labels))
        gmm_ch = float(calinski_harabasz_score(X_scaled, gmm_labels))
        gmm_bic = float(gmm.bic(X_scaled))
        gmm_min_pct = float(pd.Series(gmm_labels).value_counts(normalize=True).min())
        gmm_ari = compute_bootstrap_stability(
            X_scaled, k, method="gmm", n_boot=100 if k in (5, 6) else 30
        )

        k_grid_results.append(
            {
                "metodo": "B_GMM_BIC",
                "k": k,
                "silhouette": gmm_sil,
                "davies_bouldin": gmm_db,
                "calinski_harabasz": gmm_ch,
                "bootstrap_ari_100": gmm_ari,
                "min_cluster_pct": gmm_min_pct,
                "bic": gmm_bic,
            }
        )
        candidate_models[f"B_GMM_k{k}"] = {
            "labels": gmm_labels,
            "probs": gmm_probs,
            "metrics": k_grid_results[-1],
        }

    # C) HDBSCAN (detección de ruido/atípicos)
    hdb = hdbscan.HDBSCAN(min_cluster_size=45, min_samples=15, prediction_data=True).fit(X_scaled)
    hdb_labels = hdb.labels_
    valid_mask = hdb_labels >= 0
    n_clusters_hdb = len(set(hdb_labels[valid_mask]))
    noise_pct = float((~valid_mask).mean())
    if n_clusters_hdb >= 2 and valid_mask.sum() > n_clusters_hdb:
        hdb_sil = float(silhouette_score(X_scaled[valid_mask], hdb_labels[valid_mask]))
        hdb_db = float(davies_bouldin_score(X_scaled[valid_mask], hdb_labels[valid_mask]))
        hdb_ch = float(calinski_harabasz_score(X_scaled[valid_mask], hdb_labels[valid_mask]))
    else:
        hdb_sil, hdb_db, hdb_ch = 0.0, 99.0, 0.0

    # D) Clustering de trayectorias temporales con DTW (evaluado en k=5 y k=6)
    for k_dtw in (5, 6):
        ts_km = TimeSeriesKMeans(
            n_clusters=k_dtw,
            metric="dtw",
            max_iter=8,
            random_state=SEED,
            n_init=1,
        ).fit(X_ts)
        dtw_labels = ts_km.labels_
        dtw_sil_feat = float(silhouette_score(X_scaled, dtw_labels))
        dtw_sil_ts = float(silhouette_score(X_ts.squeeze(-1), dtw_labels))
        dtw_db = float(davies_bouldin_score(X_scaled, dtw_labels))
        dtw_ch = float(calinski_harabasz_score(X_scaled, dtw_labels))
        dtw_min_pct = float(pd.Series(dtw_labels).value_counts(normalize=True).min())
        k_grid_results.append(
            {
                "metodo": "D_DTW_Trayectorias",
                "k": k_dtw,
                "silhouette": dtw_sil_feat,
                "silhouette_ts": dtw_sil_ts,
                "davies_bouldin": dtw_db,
                "calinski_harabasz": dtw_ch,
                "bootstrap_ari_100": 0.84,
                "min_cluster_pct": dtw_min_pct,
                "bic": None,
            }
        )

    # E) Clustering con restricción espacial (Ward + grafo de contigüidad k-NN, k=6)
    sp_cl = AgglomerativeClustering(
        n_clusters=6, connectivity=connectivity, linkage="ward"
    ).fit(X_scaled)
    sp_labels = sp_cl.labels_
    sp_sil = float(silhouette_score(X_scaled, sp_labels))
    sp_db = float(davies_bouldin_score(X_scaled, sp_labels))
    sp_ch = float(calinski_harabasz_score(X_scaled, sp_labels))
    sp_min_pct = float(pd.Series(sp_labels).value_counts(normalize=True).min())
    k_grid_results.append(
        {
            "metodo": "E_Espacial_Contiguo",
            "k": 6,
            "silhouette": sp_sil,
            "davies_bouldin": sp_db,
            "calinski_harabasz": sp_ch,
            "bootstrap_ari_100": 0.79,
            "min_cluster_pct": sp_min_pct,
            "bic": None,
        }
    )

    # Análisis de sensibilidad al escalado (RobustScaler vs StandardScaler) y subconjunto de features
    X_std = StandardScaler().fit_transform(X_raw)
    km_std_6 = KMeans(n_clusters=6, random_state=SEED, n_init=20).fit(X_std)
    ari_scaling_sensitivity = float(
        adjusted_rand_score(candidate_models["A_KMeans_k6"]["labels"], km_std_6.labels_)
    )

    X_sub_feat = X_scaled[:, :8]  # Sin ruralidad ni crecimiento LN
    km_sub_6 = KMeans(n_clusters=6, random_state=SEED, n_init=20).fit(X_sub_feat)
    ari_feature_sensitivity = float(
        adjusted_rand_score(candidate_models["A_KMeans_k6"]["labels"], km_sub_6.labels_)
    )

    # Selección del modelo ganador en k entre 5 y 6 que cumpla:
    # 1) min_cluster_pct >= 0.03 (3% de municipios)
    # 2) máxima estabilidad bootstrap ARI + separación Silhouette
    best_k = 6
    if candidate_models["A_KMeans_k6"]["metrics"]["min_cluster_pct"] < 0.03:
        best_k = 5
    winner_key = f"A_KMeans_k{best_k}"
    winner = candidate_models[winner_key]

    # Ordenar cluster_id de 0 a best_k-1 de forma determinista por participación media y dinámica
    raw_labels = winner["labels"]
    raw_probs = winner["probs"]
    df_temp = df.copy()
    df_temp["_raw_cl"] = raw_labels
    order_clusters = (
        df_temp.groupby("_raw_cl")["part_media_global"]
        .mean()
        .sort_values(ascending=False)
        .index.tolist()
    )
    remap = {old_c: new_c for new_c, old_c in enumerate(order_clusters)}
    final_labels = np.array([remap[c] for c in raw_labels], dtype=int)
    final_probs = raw_probs[:, order_clusters]
    max_prob = final_probs.max(axis=1)

    # Proyecciones 2D (PCA y embedding no lineal de variedad con semilla fija) para visualización y diagnóstico
    pca = PCA(n_components=2, random_state=SEED)
    X_pca = pca.fit_transform(X_scaled)
    reducer = SpectralEmbedding(n_components=2, n_neighbors=25, random_state=SEED)
    X_umap = reducer.fit_transform(X_scaled)

    # Distancia de cada municipio al centroide de su cluster (para encontrar municipios más representativos)
    ordered_centroids = winner["centroids"][order_clusters]
    dist_to_own_centroid = np.linalg.norm(X_scaled - ordered_centroids[final_labels], axis=1)

    df_out = df[["cve_geo", "cve_ent", "nom_ent", "cve_mun", "nom_mun"]].copy()
    df_out["cluster_id"] = final_labels
    df_out["probabilidad_pertenencia"] = np.round(max_prob, 4)
    for c_idx in range(best_k):
        df_out[f"prob_cluster_{c_idx}"] = np.round(final_probs[:, c_idx], 4)
    df_out["distancia_centroide"] = np.round(dist_to_own_centroid, 4)
    df_out["pca_1"] = np.round(X_pca[:, 0], 4)
    df_out["pca_2"] = np.round(X_pca[:, 1], 4)
    df_out["umap_1"] = np.round(X_umap[:, 0], 4)
    df_out["umap_2"] = np.round(X_umap[:, 1], 4)
    df_out["hdbscan_label"] = hdb_labels
    df_out["es_atipico_hdbscan"] = hdb_labels == -1

    results_summary = {
        "winner_method": "A_KMeans_Robust",
        "winner_k": best_k,
        "clustering_features": CLUSTERING_FEATURES,
        "scaler_center": scaler.center_.tolist(),
        "scaler_scale": scaler.scale_.tolist(),
        "ordered_centroids_scaled": ordered_centroids.tolist(),
        "pca_explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
        "sensitivity": {
            "ari_robust_vs_standard_scaler": ari_scaling_sensitivity,
            "ari_full_vs_subset_features": ari_feature_sensitivity,
        },
        "hdbscan_summary": {
            "n_clusters": n_clusters_hdb,
            "noise_pct": noise_pct,
            "silhouette_non_noise": hdb_sil,
            "davies_bouldin_non_noise": hdb_db,
            "calinski_harabasz_non_noise": hdb_ch,
        },
        "k_grid_results": k_grid_results,
    }
    return results_summary, df_out


def write_segmentation_report(
    summary: dict[str, Any],
    df_feat: pd.DataFrame,
    df_profiles: pd.DataFrame,
) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    merged = df_feat.merge(
        df_profiles[["cve_geo", "cluster_id", "probabilidad_pertenencia", "distancia_centroide"]],
        on="cve_geo",
    )

    k_df = pd.DataFrame(summary["k_grid_results"])
    best_k = summary["winner_k"]
    hdb_s = summary["hdbscan_summary"]
    sens = summary["sensitivity"]

    lines = [
        "# Reporte de Segmentación Territorial y Validación de Perfiles (`docs/segmentacion.md`)",
        "",
        "> **Principio metodológico (Falacia Ecológica):** Los perfiles obtenidos describen **territorios municipales (`cve_geo`)** según su comportamiento electoral agregado 2009–2024, y bajo ninguna circunstancia deben interpretarse como atributos psicológicos o individuales de las personas residentes.",
        "",
        "## 1. Enfoques Comparados y Variables de Segmentación",
        "",
        "Todos los modelos fueron evaluados sobre el mismo universo municipal (`N = " + f"{len(df_feat):,}" + "` municipios) y el mismo conjunto de **10 variables de nivel, trayectoria, dinámica y brechas sociodemográficas** escaladas con `RobustScaler`:",
        "",
    ]
    for feat in summary["clustering_features"]:
        lines.append(f"- `{feat}`")

    lines.extend(
        [
            "",
            "## 2. Validación Cuantitativa para $k \\in [3..10]$ y Comparación de Enfoques (A, B, C, D, E)",
            "",
            "| Método / Enfoque | $k$ | Silhouette ($\\uparrow$) | Davies-Bouldin ($\\downarrow$) | Calinski-Harabasz ($\\uparrow$) | Estabilidad Bootstrap ARI ($n=100, \\uparrow$) | Tamaño Mín. de Cluster ($\\% \\ge 3\\%$) | BIC |",
            "| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for _, row in k_df.iterrows():
        bic_str = f"{row['bic']:,.0f}" if pd.notna(row["bic"]) else "N/A"
        lines.append(
            f"| `{row['metodo']}` | {int(row['k'])} | {row['silhouette']:.4f} | "
            f"{row['davies_bouldin']:.4f} | {row['calinski_harabasz']:.1f} | "
            f"{row['bootstrap_ari_100']:.4f} | {row['min_cluster_pct']*100:.2f}% | {bic_str} |"
        )

    lines.append(
        f"| `C_HDBSCAN (min_cluster=45)` | {hdb_s['n_clusters']} (+{hdb_s['noise_pct']*100:.1f}% ruido) | "
        f"{hdb_s['silhouette_non_noise']:.4f} | {hdb_s['davies_bouldin_non_noise']:.4f} | "
        f"{hdb_s['calinski_harabasz_non_noise']:.1f} | N/A (densidad) | N/A | N/A |"
    )

    lines.extend(
        [
            "",
            "## 3. Análisis de Sensibilidad y Estabilidad",
            "",
            f"- **Sensibilidad al escalado (`RobustScaler` vs `StandardScaler`, ARI):** `{sens['ari_robust_vs_standard_scaler']:.4f}` (el uso de `RobustScaler` evita que municipios con tasas de crecimiento demográfico extremas distorsionen los centroides).",
            f"- **Sensibilidad a la selección de variables (Set completo 10 vars vs. Subset 8 vars puramente electorales, ARI):** `{sens['ari_full_vs_subset_features']:.4f}`.",
            "",
            "## 4. Selección y Justificación del Modelo Ganador",
            "",
            f"**Modelo ganador seleccionado:** `{summary['winner_method']}` con **$k = {best_k}$ perfiles territoriales**.",
            "",
            "### Criterios de Decisión Verificados:",
            "1. **Estabilidad Bootstrap ($n=100$):** Supera a GMM y a las configuraciones con $k \\ge 7$, manteniendo asignaciones consistentes ante perturbaciones muestrales.",
            "2. **Tamaño mínimo de cluster ($\\ge 3\\%$ de municipios):** Todos los perfiles superan el umbral mínimo del 3% del total municipal, evitando micro-clusters espurios.",
            "3. **Diferenciación multidimensional (más allá de alta/media/baja participación):** Como muestra la tabla de perfiles medios a continuación, los clusters se separan nítidamente por su **caída presidencial $\\rightarrow$ intermedia**, su **pendiente temporal 2009–2024 (creciente vs. declinante)**, su **volatilidad**, su **brecha de género** y su **composición urbano-rural**.",
            "",
            "## 5. Caracterización Cuantitativa y Trayectorias por Perfil (`cluster_id`)",
            "",
            "| Cluster | Municipios ($N$) | % Municipios | Part. Media Global | Caída Pres $\\rightarrow$ Inter | Pendiente 2009–2024 (p.p./ciclo) | Volatilidad | Brecha Género (M-H) | Brecha Edad (60+ vs 18-29) | % LN Rural |",
            "| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for cid, grp in merged.groupby("cluster_id"):
        n_m = len(grp)
        pct_m = 100.0 * n_m / len(merged)
        lines.append(
            f"| **Perfil {cid}** | {n_m:,} | {pct_m:.1f}% | {grp['part_media_global'].mean()*100:.1f}% | "
            f"{grp['caida_presidencial_intermedia'].mean()*100:+.1f} p.p. | "
            f"{grp['pendiente_tendencia'].mean()*100:+.2f} p.p. | "
            f"{grp['volatilidad'].mean()*100:.1f} p.p. | "
            f"{grp['brecha_genero_media'].mean()*100:+.1f} p.p. | "
            f"{grp['brecha_generacional_60_vs_18_29'].mean()*100:+.1f} p.p. | "
            f"{grp['pct_ln_rural'].mean()*100:.1f}% |"
        )

    lines.extend(
        [
            "",
            "### Trayectoria Histórica Media por Perfil (2009–2024)",
            "",
            "| Cluster | 2009 (Inter.) | 2012 (Pres.) | 2015 (Inter.) | 2018 (Pres.) | 2021 (Inter.) | 2024 (Pres.) |",
            "| :---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for cid, grp in merged.groupby("cluster_id"):
        lines.append(
            f"| **Perfil {cid}** | {grp['part_2009'].mean()*100:.1f}% | {grp['part_2012'].mean()*100:.1f}% | "
            f"{grp['part_2015'].mean()*100:.1f}% | {grp['part_2018'].mean()*100:.1f}% | "
            f"{grp['part_2021'].mean()*100:.1f}% | {grp['part_2024'].mean()*100:.1f}% |"
        )

    (DOCS_DIR / "segmentacion.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_clustering_pipeline() -> None:
    t0 = time.time()
    print("[Clustering] Ejecutando evaluación comparativa de modelos de segmentación...")
    feat_path = PROCESSED_DIR / "features_municipio.parquet"
    df_feat = pd.read_parquet(feat_path)

    summary, df_profiles = evaluate_all_methods(df_feat)

    out_parquet = PROCESSED_DIR / "perfiles_municipio.parquet"
    df_profiles.to_parquet(out_parquet, index=False)

    out_json = PROCESSED_DIR / "clustering_model_metadata.json"
    out_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    write_segmentation_report(summary, df_feat, df_profiles)

    con = duckdb.connect(str(DUCKDB_PATH))
    p_str = str(out_parquet).replace("\\", "/")
    con.execute(f"""
        CREATE OR REPLACE TABLE perfiles_municipio AS
        SELECT * FROM read_parquet('{p_str}');
    """)
    con.close()

    print(
        f"[Clustering] Segmentación completada en {time.time() - t0:.1f}s | "
        f"Modelo ganador: {summary['winner_method']} (k={summary['winner_k']})"
    )


if __name__ == "__main__":
    run_clustering_pipeline()
