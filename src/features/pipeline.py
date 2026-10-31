from __future__ import annotations

import json
import time
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from esda.moran import Moran, Moran_Local
from libpysal.weights import KNN
from scipy.stats import theilslopes

from src.features.enrichment import fetch_or_load_external_enrichment

BASE_DIR = Path(__file__).resolve().parents[2]
DUCKDB_PATH = BASE_DIR / "data" / "ccpc.duckdb"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DOCS_DIR = BASE_DIR / "docs"
YEARS = [2009, 2012, 2015, 2018, 2021, 2024]

# Coordenadas aproximadas del centroide de cada Entidad Federativa (lat, lon) para construir
# vecindad espacial jerárquica reproducible cuando no se cuenta con shapefile municipal externo
ENTIDAD_COORDS: dict[str, tuple[float, float]] = {
    "01": (21.88, -102.29),
    "02": (30.84, -115.28),
    "03": (26.04, -111.67),
    "04": (19.83, -90.53),
    "05": (27.06, -101.71),
    "06": (19.12, -103.88),
    "07": (16.75, -92.64),
    "08": (28.63, -106.09),
    "09": (19.43, -99.13),
    "10": (24.56, -104.66),
    "11": (21.02, -101.26),
    "12": (17.55, -99.50),
    "13": (20.09, -98.76),
    "14": (20.66, -103.35),
    "15": (19.29, -99.66),
    "16": (19.57, -101.71),
    "17": (18.68, -99.10),
    "18": (21.75, -104.85),
    "19": (25.59, -99.99),
    "20": (17.07, -96.73),
    "21": (19.04, -98.21),
    "22": (20.59, -100.39),
    "23": (19.18, -88.48),
    "24": (22.16, -100.99),
    "25": (25.17, -107.48),
    "26": (29.30, -110.33),
    "27": (17.84, -92.62),
    "28": (24.27, -98.84),
    "29": (19.32, -98.24),
    "30": (19.17, -96.13),
    "31": (20.71, -89.10),
    "32": (22.77, -102.58),
}


def _robust_slope(values: np.ndarray, x: np.ndarray) -> float:
    mask = ~np.isnan(values)
    if mask.sum() < 2:
        return 0.0
    y_valid = values[mask]
    x_valid = x[mask]
    if np.allclose(y_valid, y_valid[0]):
        return 0.0
    slope, _, _, _ = theilslopes(y_valid, x_valid)
    return float(slope)


def compute_spatial_autocorrelation(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    """
    Calcula Moran's I global y LISA local sobre la participación media municipal.
    Utiliza coordenadas jerárquicas (entidad + distrito federal + clave municipal normalizada)
    con k-NN (k=8) y semilla fija para garantizar reproducibilidad determinista.
    """
    np.random.seed(42)
    coords = []
    for _, row in df.iterrows():
        ent = str(row["cve_ent"]).zfill(2)
        base_lat, base_lon = ENTIDAD_COORDS.get(ent, (20.0, -100.0))
        mun_num = int(row["cve_mun"])
        raw_def = "".join(ch for ch in str(row.get("def_principal", "1")) if ch.isdigit())
        def_num = int(raw_def) if raw_def else 1
        # Desplazamiento determinista sub-grado por distrito federal y clave municipal dentro de la entidad
        lat = base_lat + (def_num * 0.07) + ((mun_num % 25) * 0.015)
        lon = base_lon + ((def_num % 7) * 0.07) + ((mun_num // 25) * 0.015)
        coords.append([lon, lat])

    coords_arr = np.array(coords, dtype=float)
    w = KNN.from_array(coords_arr, k=8)
    w.transform = "r"

    y = df["part_media_global"].to_numpy(dtype=float)
    moran_global = Moran(y, w, permutations=499)
    moran_local = Moran_Local(y, w, permutations=499, seed=42)

    # Mapeo de cuadrantes LISA: 1=HH, 2=LH, 3=LL, 4=HL
    quad_map = {1: "HH (Alto-Alto)", 2: "LH (Bajo-Alto)", 3: "LL (Bajo-Bajo)", 4: "HL (Alto-Bajo)"}
    lisa_labels = []
    for q, p_val in zip(moran_local.q, moran_local.p_sim, strict=False):
        if p_val < 0.05:
            lisa_labels.append(quad_map.get(int(q), "NS"))
        else:
            lisa_labels.append("NS (No significativo)")

    df = df.copy()
    df["lat_aprox"] = coords_arr[:, 1]
    df["lon_aprox"] = coords_arr[:, 0]
    df["lisa_i"] = moran_local.Is
    df["lisa_q"] = moran_local.q
    df["lisa_p_val"] = moran_local.p_sim
    df["lisa_cluster"] = lisa_labels
    df["moran_global_i"] = float(moran_global.I)
    df["moran_global_p_val"] = float(moran_global.p_sim)

    summary = {
        "moran_global_I": float(moran_global.I),
        "moran_global_p_sim": float(moran_global.p_sim),
        "moran_global_z_sim": float(moran_global.z_sim),
        "n_municipios": len(df),
        "lisa_counts": pd.Series(lisa_labels).value_counts().to_dict(),
    }
    return df, summary


def build_features_matrix() -> pd.DataFrame:
    t0 = time.time()
    print("[Features] Construyendo matriz de features municipales 2009-2024...")

    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    mun_elec = con.execute("SELECT * FROM v_municipio_eleccion ORDER BY cve_geo, anio").df()
    bridge = con.execute("SELECT * FROM puente_municipio_anio ORDER BY cve_geo").df()
    def_mode = con.execute("""
        WITH def_sums AS (
            SELECT cve_geo, def, SUM(lista_nominal) AS ln_sum
            FROM ccpc_unificado
            WHERE modalidad = 'presencial'
            GROUP BY cve_geo, def
        )
        SELECT cve_geo, FIRST(def ORDER BY ln_sum DESC) AS def_principal
        FROM def_sums
        GROUP BY cve_geo
    """).df()
    con.close()

    # Medianas nacionales y estatales por año para constancia e imputación documentada
    nat_medians = mun_elec.groupby("anio")["participacion"].median().to_dict()
    state_medians = mun_elec.groupby(["cve_ent", "anio"])["participacion"].median().to_dict()

    mun_elec["sobre_mediana_nacional"] = mun_elec.apply(
        lambda r: float(r["participacion"] > nat_medians[int(r["anio"])]), axis=1
    )
    mun_elec["brecha_genero"] = mun_elec["part_mujeres"] - mun_elec["part_hombres"]
    mun_elec["brecha_generacional"] = mun_elec["part_60_mas"] - mun_elec["part_18_29"]

    # Pivotes por año para participación y lista nominal
    p_pivot = mun_elec.pivot(index="cve_geo", columns="anio", values="participacion")
    ln_pivot = mun_elec.pivot(index="cve_geo", columns="anio", values="lista_nominal")
    bg_pivot = mun_elec.pivot(index="cve_geo", columns="anio", values="brecha_genero")

    records = []
    # Ciclos electorales normalizados (0, 1, 2, 3, 4, 5) para pendiente por elección
    x_cycles = np.arange(len(YEARS), dtype=float)

    grouped_mun = mun_elec.groupby("cve_geo", sort=True)
    for cve_geo, grp in grouped_mun:
        first_row = grp.iloc[0]
        last_row = grp.iloc[-1]
        cve_ent = str(first_row["cve_ent"]).zfill(2)

        raw_parts = []
        imp_parts = []
        was_imputed = False
        for y in YEARS:
            val = p_pivot.loc[cve_geo, y] if y in p_pivot.columns else np.nan
            raw_parts.append(float(val) if pd.notna(val) else np.nan)
            if pd.isna(val):
                was_imputed = True
                imp_val = state_medians.get((cve_ent, y), nat_medians[y])
                imp_parts.append(float(imp_val))
            else:
                imp_parts.append(float(val))

        raw_arr = np.array(raw_parts, dtype=float)
        imp_arr = np.array(imp_parts, dtype=float)

        # Participación por tipo de elección (presidencial: 2012, 2018, 2024 | intermedia: 2009, 2015, 2021)
        pres_vals = imp_arr[[1, 3, 5]]
        inter_vals = imp_arr[[0, 2, 4]]
        part_pres = float(np.nanmean(pres_vals))
        part_inter = float(np.nanmean(inter_vals))
        part_global = float(np.nanmean(imp_arr))
        caida_pres_inter = part_pres - part_inter

        # Pendiente robusta (Theil-Sen) y volatilidad (desviación estándar)
        pendiente_part = _robust_slope(raw_arr, x_cycles)
        volatilidad_part = float(np.nanstd(raw_arr, ddof=0))
        volatilidad_inter_tipo = float(
            0.5 * (np.nanstd(pres_vals, ddof=0) + np.nanstd(inter_vals, ddof=0))
        )

        # Constancia sobre la mediana nacional
        constancia = float(grp["sobre_mediana_nacional"].mean())

        # Brecha de género (mujeres - hombres): promedio y tendencia
        bg_vals = np.array(
            [bg_pivot.loc[cve_geo, y] if y in bg_pivot.columns else np.nan for y in YEARS],
            dtype=float,
        )
        brecha_genero_media = float(np.nanmean(bg_vals)) if not np.all(np.isnan(bg_vals)) else 0.0
        brecha_genero_tendencia = _robust_slope(bg_vals, x_cycles)

        # Estructura por edad y brecha generacional directa del CCPC
        total_ln_sum = float(grp["lista_nominal"].sum())
        pct_ln_18_29 = float(grp["ln_18_29"].sum() / total_ln_sum) if total_ln_sum > 0 else 0.0
        pct_ln_60_mas = float(grp["ln_60_mas"].sum() / total_ln_sum) if total_ln_sum > 0 else 0.0
        part_media_18_29 = float(grp["part_18_29"].mean())
        part_media_30_59 = float(grp["part_30_59"].mean())
        part_media_60_mas = float(grp["part_60_mas"].mean())
        brecha_generacional_media = float(grp["brecha_generacional"].mean())

        # Urbanización electoral directa del CCPC (TIPOSEC: U, M, R)
        pct_ln_urbana = float(grp["ln_urbana"].sum() / total_ln_sum) if total_ln_sum > 0 else 0.0
        pct_ln_mixta = float(grp["ln_mixta"].sum() / total_ln_sum) if total_ln_sum > 0 else 0.0
        pct_ln_rural = float(grp["ln_rural"].sum() / total_ln_sum) if total_ln_sum > 0 else 0.0

        # Lista nominal y crecimiento 2009-2024
        ln_2009 = float(ln_pivot.loc[cve_geo, 2009]) if 2009 in ln_pivot.columns and pd.notna(ln_pivot.loc[cve_geo, 2009]) else float(first_row["lista_nominal"])
        ln_2024 = float(ln_pivot.loc[cve_geo, 2024]) if 2024 in ln_pivot.columns and pd.notna(ln_pivot.loc[cve_geo, 2024]) else float(last_row["lista_nominal"])
        ln_promedio = float(grp["lista_nominal"].mean())
        crecimiento_ln_relativo = (ln_2024 - ln_2009) / max(ln_2009, 1.0)
        n_years_span = max(int(last_row["anio"]) - int(first_row["anio"]), 1)
        cagr_ln = (ln_2024 / max(ln_2009, 1.0)) ** (1.0 / n_years_span) - 1.0

        # Adopción del voto anticipado 2024
        row_2024 = grp[grp["anio"] == 2024]
        vot_ant_2024 = int(row_2024["votantes_anticipado"].iloc[0]) if not row_2024.empty else 0
        tasa_va_10k = (vot_ant_2024 * 10000.0) / max(ln_2024, 1.0)

        n_obs = int((~np.isnan(raw_arr)).sum())
        # Regla explícita de baja confiabilidad: LN promedio < 1,000 electores o panel incompleto (< 6 elecciones)
        baja_confiabilidad = bool((ln_promedio < 1000.0) or (n_obs < 6))

        records.append(
            {
                "cve_geo": cve_geo,
                "cve_ent": cve_ent,
                "nom_ent": str(last_row["nom_ent"]),
                "cve_mun": str(last_row["cve_mun"]).zfill(3),
                "nom_mun": str(last_row["nom_mun"]),
                "n_elecciones_observadas": n_obs,
                "flag_imputacion_trayectoria": was_imputed,
                "flag_baja_confiabilidad": baja_confiabilidad,
                # Serie temporal imputada (para modelos matriciales/DTW sin NaN)
                "part_2009": imp_parts[0],
                "part_2012": imp_parts[1],
                "part_2015": imp_parts[2],
                "part_2018": imp_parts[3],
                "part_2021": imp_parts[4],
                "part_2024": imp_parts[5],
                # Serie temporal observada cruda (con NaN si el municipio no existía)
                "part_2009_raw": raw_parts[0],
                "part_2012_raw": raw_parts[1],
                "part_2015_raw": raw_parts[2],
                "part_2018_raw": raw_parts[3],
                "part_2021_raw": raw_parts[4],
                "part_2024_raw": raw_parts[5],
                # Métricas agregadas de participación y dinámica
                "part_media_global": part_global,
                "part_media_presidencial": part_pres,
                "part_media_intermedia": part_inter,
                "caida_presidencial_intermedia": caida_pres_inter,
                "pendiente_tendencia": pendiente_part,
                "volatilidad": volatilidad_part,
                "volatilidad_intra_tipo": volatilidad_inter_tipo,
                "constancia_sobre_mediana": constancia,
                # Género
                "brecha_genero_media": brecha_genero_media,
                "brecha_genero_tendencia": brecha_genero_tendencia,
                # Edad / Generacional (CCPC)
                "pct_ln_jovenes_18_29": pct_ln_18_29,
                "pct_ln_adultos_60_mas": pct_ln_60_mas,
                "part_media_jovenes_18_29": part_media_18_29,
                "part_media_adultos_30_59": part_media_30_59,
                "part_media_adultos_60_mas": part_media_60_mas,
                "brecha_generacional_60_vs_18_29": brecha_generacional_media,
                # Urbanización electoral (CCPC TIPOSEC)
                "pct_ln_urbana": pct_ln_urbana,
                "pct_ln_mixta": pct_ln_mixta,
                "pct_ln_rural": pct_ln_rural,
                # Lista nominal y Voto Anticipado
                "ln_2009": ln_2009,
                "ln_2024": ln_2024,
                "ln_promedio": ln_promedio,
                "crecimiento_ln_relativo": crecimiento_ln_relativo,
                "cagr_ln_2009_2024": cagr_ln,
                "votantes_anticipado_2024": vot_ant_2024,
                "tasa_voto_anticipado_por_10k": tasa_va_10k,
                # Vector serializado JSON para trazabilidad y consumo en UI
                "serie_temporal_json": json.dumps([round(x, 6) for x in imp_parts]),
            }
        )

    df_feat = pd.DataFrame(records)
    df_feat = df_feat.merge(def_mode, on="cve_geo", how="left")
    df_feat = df_feat.merge(
        bridge[["cve_geo", "estatus_marco_geografico", "primer_anio", "ultimo_anio"]],
        on="cve_geo",
        how="left",
    )

    # Enriquecimiento externo (CONAPO / INEGI)
    df_ext = fetch_or_load_external_enrichment(df_feat["cve_geo"])
    df_feat = df_feat.merge(df_ext, on="cve_geo", how="left")

    # Autocorrelación espacial (Moran's I global y LISA local)
    df_feat, spatial_summary = compute_spatial_autocorrelation(df_feat)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / "features_municipio.parquet"
    df_feat.to_parquet(out_path, index=False)

    spatial_json_path = PROCESSED_DIR / "spatial_moran_summary.json"
    spatial_json_path.write_text(json.dumps(spatial_summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # Registrar también en DuckDB para consultas directas
    con = duckdb.connect(str(DUCKDB_PATH))
    f_path_str = str(out_path).replace("\\", "/")
    con.execute(f"""
        CREATE OR REPLACE TABLE features_municipio AS
        SELECT * FROM read_parquet('{f_path_str}');
    """)
    con.close()

    print(
        f"[Features] Matriz generada en {time.time() - t0:.1f}s: "
        f"{len(df_feat):,} municipios × {df_feat.shape[1]} columnas | "
        f"Moran's I global = {spatial_summary['moran_global_I']:.4f} (p={spatial_summary['moran_global_p_sim']:.4f})"
    )
    return df_feat


if __name__ == "__main__":
    build_features_matrix()
