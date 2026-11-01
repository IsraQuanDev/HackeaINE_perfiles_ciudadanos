from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import duckdb
import lightgbm as lgb
import numpy as np
import pandas as pd
import shap
from scipy.spatial.distance import cdist
from scipy.stats import theilslopes
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier, export_text

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DOCS_DIR = BASE_DIR / "docs"
DUCKDB_PATH = BASE_DIR / "data" / "ccpc.duckdb"
SEED = 42

WINDOWS = [
    ("2009-2015", [2009, 2012, 2015]),
    ("2012-2018", [2012, 2015, 2018]),
    ("2015-2021", [2015, 2018, 2021]),
    ("2018-2024", [2018, 2021, 2024]),
]

AGE_8_COLS = [
    "part_edad_18_19",
    "part_edad_20_24",
    "part_edad_25_29",
    "part_edad_30_39",
    "part_edad_40_49",
    "part_edad_50_59",
    "part_edad_60_69",
    "part_edad_70_mas",
]
AGE_8_LABELS = ["18-19", "20-24", "25-29", "30-39", "40-49", "50-59", "60-69", "70+"]


def compute_shap_and_surrogate_trees(
    df_feat: pd.DataFrame,
    df_prof: pd.DataFrame,
    feature_cols: list[str],
) -> dict[str, Any]:
    """Entrena un árbol de decisión poco profundo y un LightGBM sustituto sobre cluster_id y calcula SHAP global y por cluster."""
    X = df_feat[feature_cols].copy()
    y = df_prof["cluster_id"].to_numpy(dtype=int)
    n_clusters = int(y.max() + 1)

    dt = DecisionTreeClassifier(max_depth=3, min_samples_leaf=30, random_state=SEED)
    dt.fit(X, y)
    dt_acc = float(accuracy_score(y, dt.predict(X)))
    dt_rules_text = export_text(dt, feature_names=feature_cols)

    lgbm = lgb.LGBMClassifier(
        n_estimators=120,
        max_depth=4,
        num_leaves=15,
        learning_rate=0.08,
        random_state=SEED,
        verbose=-1,
    )
    lgbm.fit(X, y)
    lgbm_acc = float(accuracy_score(y, lgbm.predict(X)))

    explainer = shap.TreeExplainer(lgbm)
    shap_values = explainer.shap_values(X)

    if isinstance(shap_values, list):
        shap_arr = np.stack(shap_values, axis=-1)
    else:
        shap_arr = np.asarray(shap_values)
        if shap_arr.ndim == 2:
            shap_arr = shap_arr[:, :, np.newaxis]

    global_mean_abs = np.mean(np.abs(shap_arr), axis=(0, 2))
    global_ranking = sorted(
        zip(feature_cols, global_mean_abs.tolist(), strict=False),
        key=lambda t: t[1],
        reverse=True,
    )

    per_cluster_shap: dict[int, list[dict[str, Any]]] = {}
    nat_means = X.mean()
    nat_stds = X.std().replace(0, 1.0)

    for cid in range(n_clusters):
        mask = y == cid
        mean_abs_c = np.mean(np.abs(shap_arr[mask, :, cid]), axis=0)
        c_means = X.loc[mask].mean()
        c_zscores = (c_means - nat_means) / nat_stds

        ranked_vars = []
        for f_idx, fname in enumerate(feature_cols):
            ranked_vars.append(
                {
                    "feature": fname,
                    "mean_abs_shap": round(float(mean_abs_c[f_idx]), 5),
                    "cluster_mean": round(float(c_means[fname]), 5),
                    "national_mean": round(float(nat_means[fname]), 5),
                    "z_score_vs_nacional": round(float(c_zscores[fname]), 4),
                    "direccion": "ALTA (+)" if c_zscores[fname] >= 0 else "BAJA (-)",
                }
            )
        ranked_vars.sort(key=lambda d: d["mean_abs_shap"], reverse=True)
        per_cluster_shap[cid] = ranked_vars

    return {
        "decision_tree_accuracy": dt_acc,
        "decision_tree_rules": dt_rules_text,
        "lgbm_accuracy": lgbm_acc,
        "global_shap_ranking": [
            {"feature": f, "mean_abs_shap": round(val, 5)} for f, val in global_ranking
        ],
        "per_cluster_shap": per_cluster_shap,
    }


def build_cluster_characterization_json(
    df_feat: pd.DataFrame,
    df_prof: pd.DataFrame,
    feature_cols: list[str],
    shap_info: dict[str, Any],
) -> dict[str, Any]:
    """
    Genera data/processed/perfiles_caracterizacion.json con todas las estadísticas trazables,
    bandas de percentiles P10-P90, curva de participación por los 8 grupos de edad,
    retención del primer voto y el municipio prototipo REAL (medoide) por perfil.
    """
    merged = df_feat.merge(
        df_prof[
            [
                "cve_geo",
                "cluster_id",
                "probabilidad_pertenencia",
                "distancia_centroide",
                "es_atipico_hdbscan",
            ]
        ],
        on="cve_geo",
    )

    all_stat_cols = list(
        dict.fromkeys(
            feature_cols
            + [
                "part_2009",
                "part_2012",
                "part_2015",
                "part_2018",
                "part_2021",
                "part_2024",
                "part_media_presidencial",
                "part_media_intermedia",
                "part_media_jovenes_18_29",
                "part_media_adultos_30_59",
                "part_media_adultos_60_mas",
                "brecha_generacional_60_vs_18_29",
                "brecha_juvenil_18_29_vs_30_59",
                "brecha_adultos_mayores_60_vs_30_59",
                "retencion_primer_voto",
                "edad_pico_participacion",
                "pct_ln_jovenes_18_29",
                "pct_ln_adultos_60_mas",
                "pct_ln_urbana",
                "pct_ln_mixta",
                "pct_ln_rural",
                "ln_2024",
                "tasa_voto_anticipado_por_10k",
                *AGE_8_COLS,
            ]
        )
    )

    nat_means = merged[all_stat_cols].mean()
    nat_stds = merged[all_stat_cols].std().replace(0, 1.0)
    total_ln_2024_nac = float(merged["ln_2024"].sum())
    total_mun_nac = len(merged)

    national_baseline = {
        "n_municipios_nacional": total_mun_nac,
        "lista_nominal_2024_nacional": int(round(total_ln_2024_nac)),
        "medias_nacionales": {col: round(float(nat_means[col]), 6) for col in all_stat_cols},
        "trayectoria_nacional_media": {
            str(y): round(float(merged[f"part_{y}"].mean()), 6)
            for y in [2009, 2012, 2015, 2018, 2021, 2024]
        },
        "trayectoria_nacional_pct": {
            str(y): round(float(merged[f"part_{y}"].mean()) * 100.0, 2)
            for y in [2009, 2012, 2015, 2018, 2021, 2024]
        },
        "curva_edad_8grupos_nacional_pct": {
            lbl: round(float(merged[col].mean()) * 100.0, 2)
            for lbl, col in zip(AGE_8_LABELS, AGE_8_COLS, strict=True)
        },
    }

    clusters_out: list[dict[str, Any]] = []
    for cid, grp in merged.groupby("cluster_id", sort=True):
        cid_int = int(cid)
        n_mun = len(grp)
        ln_2024_sum = int(round(float(grp["ln_2024"].sum())))
        pct_mun = round(100.0 * n_mun / total_mun_nac, 2)
        pct_ln = round(100.0 * ln_2024_sum / max(total_ln_2024_nac, 1.0), 2)

        feat_stats: dict[str, Any] = {}
        for col in all_stat_cols:
            s = grp[col].dropna()
            mean_v = float(s.mean())
            z_v = float((mean_v - nat_means[col]) / nat_stds[col])
            q10, q25, q50, q75, q90 = np.percentile(s, [10, 25, 50, 75, 90])
            is_pct_col = col.startswith(
                ("part_", "pct_", "caida_", "brecha_", "volatilidad", "constancia", "pendiente", "cagr", "retencion_", "rezago_")
            )
            feat_stats[col] = {
                "media": round(mean_v, 6),
                "media_pct": round(mean_v * 100.0, 2) if is_pct_col else round(mean_v, 2),
                "p10": round(float(q10), 6),
                "p25": round(float(q25), 6),
                "p50_mediana": round(float(q50), 6),
                "p75": round(float(q75), 6),
                "p90": round(float(q90), 6),
                "z_score_vs_nacional": round(z_v, 4),
            }

        ent_counts = grp.groupby(["cve_ent", "nom_ent"]).size().sort_values(ascending=False).head(5)
        entidades_pred = [
            {
                "cve_ent": str(k[0]),
                "nom_ent": str(k[1]),
                "n_municipios_en_cluster": int(v),
                "pct_del_cluster": round(100.0 * int(v) / n_mun, 2),
            }
            for k, v in ent_counts.items()
        ]

        rep_muns = grp.sort_values("distancia_centroide", ascending=True).head(10)
        municipios_rep = [
            {
                "cve_geo": str(r["cve_geo"]),
                "nom_mun": str(r["nom_mun"]),
                "nom_ent": str(r["nom_ent"]),
                "distancia_centroide": round(float(r["distancia_centroide"]), 4),
                "part_media_global": round(float(r["part_media_global"]), 4),
                "part_media_global_pct": round(float(r["part_media_global"]) * 100.0, 2),
                "ln_2024": int(round(float(r["ln_2024"]))),
            }
            for _, r in rep_muns.iterrows()
        ]

        medoid_mun = municipios_rep[0]

        clusters_out.append(
            {
                "cluster_id": cid_int,
                "n_municipios": n_mun,
                "pct_municipios_nacional": pct_mun,
                "poblacion_lista_nominal_2024": ln_2024_sum,
                "pct_lista_nominal_nacional": pct_ln,
                "n_municipios_baja_confiabilidad": int(grp["flag_baja_confiabilidad"].sum()),
                "pct_baja_confiabilidad": round(100.0 * float(grp["flag_baja_confiabilidad"].mean()), 2),
                "municipio_prototipo_medoide": medoid_mun,
                "top_5_variables_definitorias_shap": shap_info["per_cluster_shap"][cid_int][:5],
                "entidades_predominantes": entidades_pred,
                "municipios_mas_representativos": municipios_rep,
                "trayectoria_media": {
                    str(y): round(float(grp[f"part_{y}"].mean()), 6)
                    for y in [2009, 2012, 2015, 2018, 2021, 2024]
                },
                "trayectoria_media_pct": {
                    str(y): round(float(grp[f"part_{y}"].mean()) * 100.0, 2)
                    for y in [2009, 2012, 2015, 2018, 2021, 2024]
                },
                "trayectoria_p10_pct": {
                    str(y): round(float(np.percentile(grp[f"part_{y}"], 10)) * 100.0, 2)
                    for y in [2009, 2012, 2015, 2018, 2021, 2024]
                },
                "trayectoria_p90_pct": {
                    str(y): round(float(np.percentile(grp[f"part_{y}"], 90)) * 100.0, 2)
                    for y in [2009, 2012, 2015, 2018, 2021, 2024]
                },
                "curva_edad_8grupos_pct": {
                    lbl: round(float(grp[col].mean()) * 100.0, 2)
                    for lbl, col in zip(AGE_8_LABELS, AGE_8_COLS, strict=True)
                },
                "estadisticas_features": feat_stats,
            }
        )

    return {
        "nota_metodologica": (
            "Los perfiles describen TERRITORIOS municipales (cve_geo) basados en conteos censales "
            "agregados 2009-2024 del INE con participación definida como SV/(SV+NV) y cobertura >= 90%, "
            "nunca individuos (prevención de falacia ecológica)."
        ),
        "convencion_signo_caida": (
            "Caída Presidencial -> Intermedia = Participación Media Presidencial - Participación Media Intermedia. "
            "Un valor positivo (+p.p.) indica que la elección intermedia tuvo menor participación que la presidencial; "
            "un valor negativo (-p.p.) indica que la elección intermedia superó en participación a la presidencial."
        ),
        "referencia_nacional": national_baseline,
        "explicabilidad_global": {
            "decision_tree_accuracy": round(shap_info["decision_tree_accuracy"], 4),
            "lgbm_accuracy": round(shap_info["lgbm_accuracy"], 4),
            "global_shap_ranking": shap_info["global_shap_ranking"],
        },
        "perfiles": clusters_out,
    }


def compute_temporal_window_transitions(
    df_feat: pd.DataFrame,
    meta: dict[str, Any],
) -> dict[str, Any]:
    """
    Recalcula las métricas de cada municipio en las 4 ventanas móviles
    (2009-2015, 2012-2018, 2015-2021, 2018-2024), construye la Cadena de Markov
    (matriz de probabilidades de transición), el grafo DAG acíclico para Sankey
    y la tabla de municipios que cambiaron de perfil EXCLUYENDO aquellos con datos
    faltantes o baja cobertura NS.
    """
    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    mun_elec = con.execute("SELECT * FROM v_municipio_eleccion ORDER BY cve_geo, anio").df()
    con.close()

    nat_medians = mun_elec.groupby("anio")["participacion"].median().to_dict()
    mun_elec["sobre_mediana"] = mun_elec.apply(
        lambda r: float(r["participacion"] > nat_medians[int(r["anio"])])
        if pd.notna(r["participacion"])
        else np.nan,
        axis=1,
    )
    mun_elec["brecha_genero"] = mun_elec["part_mujeres"] - mun_elec["part_hombres"]

    feature_cols: list[str] = meta["clustering_features"]
    center = np.array(meta["scaler_center"], dtype=float)
    scale = np.array(meta["scaler_scale"], dtype=float)
    centroids = np.array(meta["ordered_centroids_scaled"], dtype=float)

    base_static = df_feat.set_index("cve_geo")
    window_assignments: dict[str, pd.Series] = {}

    for w_name, w_years in WINDOWS:
        sub = mun_elec[mun_elec["anio"].isin(w_years)]
        p_piv = sub.pivot(index="cve_geo", columns="anio", values="participacion")
        bg_piv = sub.pivot(index="cve_geo", columns="anio", values="brecha_genero")
        const_s = sub.groupby("cve_geo")["sobre_mediana"].mean()

        rows_w = []
        for cve_geo in df_feat["cve_geo"]:
            vals = []
            for y in w_years:
                v = p_piv.loc[cve_geo, y] if (cve_geo in p_piv.index and y in p_piv.columns) else np.nan
                if pd.isna(v):
                    v = base_static.loc[cve_geo, f"part_{y}"]
                vals.append(float(v))
            arr = np.array(vals, dtype=float)

            pres_v = [vals[i] for i, y in enumerate(w_years) if y in (2012, 2018, 2024)]
            inter_v = [vals[i] for i, y in enumerate(w_years) if y in (2009, 2015, 2021)]

            p_glob = float(np.mean(arr))
            caida_pi = float(np.mean(pres_v) - np.mean(inter_v))
            slope_w, _, _, _ = theilslopes(arr, np.arange(len(w_years), dtype=float))
            vol_w = float(np.std(arr, ddof=0))
            const_w = float(
                const_s.get(cve_geo, base_static.loc[cve_geo, "constancia_sobre_mediana"])
            )
            if np.isnan(const_w):
                const_w = float(base_static.loc[cve_geo, "constancia_sobre_mediana"])

            bg_vals = [
                float(bg_piv.loc[cve_geo, y])
                if (cve_geo in bg_piv.index and y in bg_piv.columns and pd.notna(bg_piv.loc[cve_geo, y]))
                else float(base_static.loc[cve_geo, "brecha_genero_media"])
                for y in w_years
            ]
            bg_mean = float(np.mean(bg_vals))
            bg_slope, _, _, _ = theilslopes(bg_vals, np.arange(len(w_years), dtype=float))

            feat_vec = {
                "part_media_global": p_glob,
                "caida_presidencial_intermedia": caida_pi,
                "pendiente_tendencia": float(slope_w),
                "volatilidad": vol_w,
                "constancia_sobre_mediana": const_w,
                "brecha_genero_media": bg_mean,
                "brecha_genero_tendencia": float(bg_slope),
                "brecha_generacional_60_vs_18_29": float(
                    base_static.loc[cve_geo, "brecha_generacional_60_vs_18_29"]
                ),
                "brecha_juvenil_18_29_vs_30_59": float(
                    base_static.loc[cve_geo, "brecha_juvenil_18_29_vs_30_59"]
                ),
                "retencion_primer_voto": float(
                    base_static.loc[cve_geo, "retencion_primer_voto"]
                ),
                "pct_ln_rural": float(base_static.loc[cve_geo, "pct_ln_rural"]),
                "rezago_espacial_part": float(
                    base_static.loc[cve_geo, "rezago_espacial_part"]
                ),
                "cagr_ln_2009_2024": float(base_static.loc[cve_geo, "cagr_ln_2009_2024"]),
            }
            rows_w.append([feat_vec[c] for c in feature_cols])

        X_w = np.array(rows_w, dtype=float)
        X_w_scaled = np.clip((X_w - center) / scale, -3.5, 3.5)
        dists = cdist(X_w_scaled, centroids, metric="euclidean")
        labels_w = np.argmin(dists, axis=1)
        window_assignments[w_name] = pd.Series(labels_w, index=df_feat["cve_geo"], name=w_name)

    win_df = pd.DataFrame(window_assignments).reset_index()
    win_df = df_feat[
        [
            "cve_geo",
            "nom_ent",
            "nom_mun",
            "part_2009",
            "part_2024",
            "part_2009_raw",
            "part_2024_raw",
            "n_elecciones_baja_cobertura_ns",
            "flag_imputacion_trayectoria",
            "tiene_cambio_estructural_pelt",
            "anio_cambio_estructural_pelt",
            "ln_2024",
        ]
    ].merge(win_df, on="cve_geo")

    # Construcción de nodos (con nombre único por ventana para garantizar DAG acíclico en ECharts) y enlaces Sankey
    n_clusters = centroids.shape[0]
    nodes = []
    for w_name, _ in WINDOWS:
        for cid in range(n_clusters):
            nodes.append(
                {
                    "id": f"{w_name}_C{cid}",
                    "name": f"{w_name}_C{cid}",
                    "ventana": w_name,
                    "cluster_id": cid,
                    "label": f"Perfil {cid} ({w_name})",
                }
            )

    links = []
    transition_matrices: dict[str, Any] = {}
    agg_counts_mat = np.zeros((n_clusters, n_clusters), dtype=float)

    for idx in range(len(WINDOWS) - 1):
        w_from = WINDOWS[idx][0]
        w_to = WINDOWS[idx + 1][0]
        ct = pd.crosstab(win_df[w_from], win_df[w_to])
        mat_dict: dict[str, dict[str, int]] = {}
        for c_src in range(n_clusters):
            mat_dict[f"Perfil_{c_src}"] = {}
            for c_dst in range(n_clusters):
                val = int(ct.loc[c_src, c_dst]) if (c_src in ct.index and c_dst in ct.columns) else 0
                mat_dict[f"Perfil_{c_src}"][f"Perfil_{c_dst}"] = val
                agg_counts_mat[c_src, c_dst] += val
                if val > 0:
                    links.append(
                        {
                            "source": f"{w_from}_C{c_src}",
                            "target": f"{w_to}_C{c_dst}",
                            "ventana_origen": w_from,
                            "ventana_destino": w_to,
                            "cluster_origen": c_src,
                            "cluster_destino": c_dst,
                            "value": val,
                        }
                    )
        transition_matrices[f"{w_from}_a_{w_to}"] = mat_dict

    # Matriz de transición de Cadena de Markov (probabilidades por fila) y prueba de permanencia vs. azar
    row_sums = agg_counts_mat.sum(axis=1, keepdims=True)
    markov_prob_mat = np.divide(agg_counts_mat, np.maximum(row_sums, 1.0))
    permanencia_diagonal = float(np.mean(np.diag(markov_prob_mat)))
    azar_uniforme = 1.0 / max(n_clusters, 1)

    # Identificar municipios que cambiaron de perfil entre 2009-2015 y 2018-2024
    # REGLA A1.3: Excluir de la tabla de cambios reales cualquier municipio con datos faltantes / baja cobertura NS
    w_first = WINDOWS[0][0]
    w_last = WINDOWS[-1][0]
    win_df["cambio_perfil_extremos"] = win_df[w_first] != win_df[w_last]
    win_df["delta_part_2009_2024"] = win_df["part_2024_raw"] - win_df["part_2009_raw"]
    n_changed = int(win_df["cambio_perfil_extremos"].sum())
    pct_changed = round(100.0 * n_changed / len(win_df), 2)

    valid_real_change_mask = (
        win_df["cambio_perfil_extremos"]
        & win_df["part_2009_raw"].notna()
        & win_df["part_2024_raw"].notna()
        & (win_df["n_elecciones_baja_cobertura_ns"] == 0)
        & (~win_df["flag_imputacion_trayectoria"])
        & (win_df["ln_2024"] >= 1500)
    )
    changed_clean_df = win_df[valid_real_change_mask].copy()
    changed_clean_df["abs_delta"] = changed_clean_df["delta_part_2009_2024"].abs()
    top_movers = changed_clean_df.sort_values(["abs_delta", "ln_2024"], ascending=[False, False]).head(25)

    top_movers_list = [
        {
            "cve_geo": str(r["cve_geo"]),
            "nom_mun": str(r["nom_mun"]),
            "nom_ent": str(r["nom_ent"]),
            "perfil_2009_2015": int(r[w_first]),
            "perfil_2012_2018": int(r["2012-2018"]),
            "perfil_2015_2021": int(r["2015-2021"]),
            "perfil_2018_2024": int(r[w_last]),
            "part_2009_pct": round(float(r["part_2009_raw"]) * 100.0, 2),
            "part_2024_pct": round(float(r["part_2024_raw"]) * 100.0, 2),
            "delta_2009_2024_pp": round(float(r["delta_part_2009_2024"]) * 100.0, 2),
            "tiene_cambio_estructural_pelt": bool(r["tiene_cambio_estructural_pelt"]),
            "ln_2024": int(round(float(r["ln_2024"]))),
        }
        for _, r in top_movers.iterrows()
    ]

    all_changed_df = win_df[win_df["cambio_perfil_extremos"]].copy()
    ct_ext = (
        all_changed_df.groupby([w_first, w_last])
        .size()
        .reset_index(name="n_municipios")
        .sort_values("n_municipios", ascending=False)
    )
    top_flows = [
        {
            "cluster_origen_2009_2015": int(r[w_first]),
            "cluster_destino_2018_2024": int(r[w_last]),
            "n_municipios": int(r["n_municipios"]),
        }
        for _, r in ct_ext.head(10).iterrows()
    ]

    win_parquet_path = PROCESSED_DIR / "ventanas_perfiles_municipio.parquet"
    win_df.to_parquet(win_parquet_path, index=False)

    return {
        "ventanas": [w[0] for w in WINDOWS],
        "resumen_cambios": {
            "total_municipios": len(win_df),
            "municipios_cambiaron_2009_2015_vs_2018_2024": n_changed,
            "pct_municipios_cambiaron": pct_changed,
            "municipios_estables": len(win_df) - n_changed,
            "permanencia_media_diagonal_markov": round(permanencia_diagonal, 4),
            "permanencia_azar_uniforme": round(azar_uniforme, 4),
            "ratio_permanencia_vs_azar": round(permanencia_diagonal / azar_uniforme, 2),
        },
        "matriz_markov_probabilidades": [
            [round(float(val), 4) for val in row] for row in markov_prob_mat
        ],
        "top_flujos_cambio": top_flows,
        "top_municipios_cambio": top_movers_list,
        "matrices_transicion": transition_matrices,
        "sankey": {
            "nodes": nodes,
            "links": links,
        },
    }


def write_explainability_report(
    char_json: dict[str, Any],
    trans_json: dict[str, Any],
    shap_info: dict[str, Any],
) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Explicabilidad de Perfiles, Medoides Reales y Dinámica Markoviana (`docs/explicabilidad.md` · v2)",
        "",
        "## 1. Modelos Sustitutos de Explicabilidad Global (Árbol de Decisión + LightGBM SHAP)",
        "",
        f"- **Exactitud del Árbol de Decisión interpretable (`max_depth=3`):** `{shap_info['decision_tree_accuracy']*100:.2f}%`",
        f"- **Exactitud del modelo LightGBM sustituto + TreeExplainer SHAP:** `{shap_info['lgbm_accuracy']*100:.2f}%`",
        "",
        "### Ranking Global de Importancia SHAP (`mean(|SHAP|)`)",
        "",
        "| Orden | Variable | Importancia Media Absoluta SHAP |",
        "| :---: | :--- | ---: |",
    ]
    for idx, item in enumerate(shap_info["global_shap_ranking"], start=1):
        lines.append(f"| {idx} | `{item['feature']}` | `{item['mean_abs_shap']:.5f}` |")

    lines.extend(
        [
            "",
            "### Reglas del Árbol de Decisión de Poca Profundidad (`max_depth=3`)",
            "",
            "```text",
            shap_info["decision_tree_rules"].strip(),
            "```",
            "",
            "---",
            "",
            "## 2. Variables Definitorias (SHAP), Curvas de Edad y Municipio Prototipo Real (Medoide)",
            "",
        ]
    )

    for p in char_json["perfiles"]:
        cid = p["cluster_id"]
        med = p["municipio_prototipo_medoide"]
        lines.extend(
            [
                f"### Perfil {cid} ({p['n_municipios']:,} municipios — {p['pct_municipios_nacional']}% del total; Lista Nominal 2024: {p['poblacion_lista_nominal_2024']:,})",
                "",
                f"- **Municipio Prototipo Real (Medoide más cercano al centro del perfil):** **{med['nom_mun']}, {med['nom_ent']}** (`cve_geo = {med['cve_geo']}`, participación media `{med['part_media_global_pct']}%`, distancia al centroide `{med['distancia_centroide']}`).",
                "",
                "| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |",
                "| :--- | :---: | :---: | :---: | :---: | :---: |",
            ]
        )
        for v in p["top_5_variables_definitorias_shap"]:
            lines.append(
                f"| `{v['feature']}` | `{v['mean_abs_shap']:.4f}` | `{v['cluster_mean']:.4f}` | "
                f"`{v['national_mean']:.4f}` | `{v['z_score_vs_nacional']:+.2f}` | {v['direccion']} |"
            )
        lines.append("")

    res_c = trans_json["resumen_cambios"]
    lines.extend(
        [
            "---",
            "",
            "## 3. Dinámica Temporal por Ventanas Móviles y Cadena de Markov",
            "",
            f"- **Municipios evaluados:** `{res_c['total_municipios']:,}`",
            f"- **Permanencia media en la diagonal de Markov:** `{res_c['permanencia_media_diagonal_markov']*100:.1f}%` vs. `{res_c['permanencia_azar_uniforme']*100:.1f}%` bajo azar uniforme (**`{res_c['ratio_permanencia_vs_azar']}x` más estable que el azar**).",
            f"- **Municipios que cambiaron de perfil entre `2009-2015` y `2018-2024`:** `{res_c['municipios_cambiaron_2009_2015_vs_2018_2024']:,}` (`{res_c['pct_municipios_cambiaron']}%`).",
            "",
            "### Top 15 Municipios con Cambio Real de Perfil (Excluyendo Celdas con Baja Cobertura `NS`)",
            "",
            "| `cve_geo` | Municipio | Entidad | Perfil `09-15` | Perfil `18-24` | Part. 2009 (Real) | Part. 2024 (Real) | Cambio $\\Delta$ (p.p.) | Lista Nominal 2024 |",
            "| :---: | :--- | :--- | :---: | :---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for m in trans_json["top_municipios_cambio"][:15]:
        lines.append(
            f"| `{m['cve_geo']}` | {m['nom_mun']} | {m['nom_ent']} | Perfil {m['perfil_2009_2015']} | "
            f"Perfil {m['perfil_2018_2024']} | {m['part_2009_pct']:.1f}% | {m['part_2024_pct']:.1f}% | "
            f"{m['delta_2009_2024_pp']:+.1f} p.p. | {m['ln_2024']:,} |"
        )

    (DOCS_DIR / "explicabilidad.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_explain_pipeline() -> None:
    t0 = time.time()
    print("[Explain v2] Ejecutando explicabilidad SHAP, Medoides reales y Cadena de Markov entre perfiles...")

    df_feat = pd.read_parquet(PROCESSED_DIR / "features_municipio.parquet")
    df_prof = pd.read_parquet(PROCESSED_DIR / "perfiles_municipio.parquet")
    meta = json.loads((PROCESSED_DIR / "clustering_model_metadata.json").read_text(encoding="utf-8"))
    feature_cols: list[str] = meta["clustering_features"]

    shap_info = compute_shap_and_surrogate_trees(df_feat, df_prof, feature_cols)
    char_json = build_cluster_characterization_json(df_feat, df_prof, feature_cols, shap_info)
    trans_json = compute_temporal_window_transitions(df_feat, meta)

    char_path = PROCESSED_DIR / "perfiles_caracterizacion.json"
    char_path.write_text(json.dumps(char_json, indent=2, ensure_ascii=False), encoding="utf-8")

    trans_path = PROCESSED_DIR / "transiciones.json"
    trans_path.write_text(json.dumps(trans_json, indent=2, ensure_ascii=False), encoding="utf-8")

    write_explainability_report(char_json, trans_json, shap_info)
    print(f"[Explain v2] Explicabilidad y transiciones completadas en {time.time() - t0:.1f}s.")


if __name__ == "__main__":
    run_explain_pipeline()
