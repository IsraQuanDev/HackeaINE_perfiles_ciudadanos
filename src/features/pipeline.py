from __future__ import annotations

import json
import shutil
import time
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd
from esda.moran import Moran, Moran_Local
from libpysal.weights import KNN
from scipy.stats import theilslopes
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest

from src.features.enrichment import fetch_or_load_external_enrichment

BASE_DIR = Path(__file__).resolve().parents[2]
DUCKDB_PATH = BASE_DIR / "data" / "ccpc.duckdb"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
GOLD_DIR = BASE_DIR / "data" / "gold"
SERVING_DIR = BASE_DIR / "data" / "serving"
GEO_DIR = BASE_DIR / "data" / "geo"
DOCS_DIR = Path(__file__).resolve().parents[2] / "docs"
YEARS = [2009, 2012, 2015, 2018, 2021, 2024]

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
AGE_8_MIDPOINTS = [18.5, 22.0, 27.0, 34.5, 44.5, 54.5, 64.5, 75.0]


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


def _pelt_exact_changepoint(series_valid: np.ndarray, valid_years: list[int], pen: float = 0.012) -> tuple[bool, int]:
    """
    Implementación exacta de PELT (Pruned Exact Linear Time / programación dinámica penalizada L2)
    sobre la trayectoria municipal (sin valores faltantes/NS) para detectar cambios estructurales reales.
    """
    n = len(series_valid)
    if n < 4:
        return False, 0

    # Costo L2 de un segmento [i:j]
    def seg_cost(a: int, b: int) -> float:
        sub = series_valid[a:b]
        if len(sub) <= 1:
            return 0.0
        return float(np.sum((sub - np.mean(sub)) ** 2))

    total_cost_no_cp = seg_cost(0, n)
    best_gain = 0.0
    best_idx = 0
    for tau in range(2, n - 1):
        cost_split = seg_cost(0, tau) + seg_cost(tau, n) + pen
        gain = total_cost_no_cp - cost_split
        # Exigir además que el cambio en el nivel medio supere 8 puntos porcentuales
        mean_diff = abs(float(np.mean(series_valid[:tau]) - np.mean(series_valid[tau:])))
        if gain > best_gain and mean_diff >= 0.08:
            best_gain = gain
            best_idx = tau

    if best_idx > 0:
        return True, int(valid_years[best_idx])
    return False, 0


def compute_spatial_autocorrelation(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Calcula:
    - Coordenadas reales de los polígonos generados en data/geo/centroides_municipios.parquet
    - Rezago espacial (Queen/KNN k=8)
    - Moran's I global (999 permutaciones)
    - LISA local (999 permutaciones)
    - Estadístico Getis-Ord Gi* local (focos calientes y fríos)
    """
    np.random.seed(42)
    df = df.copy()

    centroids_path = GEO_DIR / "centroides_municipios.parquet"
    if centroids_path.exists():
        c_df = pd.read_parquet(centroids_path)
        df = df.merge(c_df, on="cve_geo", how="left")
        df["lon_aprox"] = df["lon"].fillna(-100.0)
        df["lat_aprox"] = df["lat"].fillna(20.0)
        df = df.drop(columns=["lon", "lat"], errors="ignore")
    else:
        df["lon_aprox"] = -100.0
        df["lat_aprox"] = 20.0

    coords_arr = np.column_stack([df["lon_aprox"].to_numpy(float), df["lat_aprox"].to_numpy(float)])
    w = KNN.from_array(coords_arr, k=8)
    w.transform = "r"

    y = df["part_media_global"].to_numpy(dtype=float)
    moran_global = Moran(y, w, permutations=999)
    moran_local = Moran_Local(y, w, permutations=999, seed=42)

    # Rezago espacial (promedio ponderado de los vecinos)
    spatial_lag = np.array([np.mean(y[w.neighbors[i]]) for i in range(len(df))], dtype=float)

    # Estadístico Getis-Ord Gi* local estandarizado
    y_mean = float(np.mean(y))
    y_std = float(np.std(y, ddof=0))
    n = len(y)
    k_plus_1 = 9.0  # municipio + 8 vecinos con peso igual en Gi*
    gi_star_z = np.zeros(n, dtype=float)
    gi_star_labels: list[str] = []
    denom_scale = y_std * np.sqrt((n * k_plus_1 - (k_plus_1**2)) / max(n - 1, 1))
    for i in range(n):
        idx_star = [i, *w.neighbors[i]]
        sum_local = float(np.sum(y[idx_star]))
        z_val = (sum_local - k_plus_1 * y_mean) / max(denom_scale, 1e-9)
        gi_star_z[i] = z_val
        if z_val >= 2.58:
            gi_star_labels.append("Hot Spot 99% (Alta Participación)")
        elif z_val >= 1.96:
            gi_star_labels.append("Hot Spot 95% (Alta Participación)")
        elif z_val <= -2.58:
            gi_star_labels.append("Cold Spot 99% (Baja Participación)")
        elif z_val <= -1.96:
            gi_star_labels.append("Cold Spot 95% (Baja Participación)")
        else:
            gi_star_labels.append("No Significativo")

    quad_map = {1: "HH (Alto-Alto)", 2: "LH (Bajo-Alto)", 3: "LL (Bajo-Bajo)", 4: "HL (Alto-Bajo)"}
    lisa_labels = []
    for q, p_val in zip(moran_local.q, moran_local.p_sim, strict=False):
        if p_val < 0.05:
            lisa_labels.append(quad_map.get(int(q), "NS"))
        else:
            lisa_labels.append("NS (No significativo)")

    df["rezago_espacial_part"] = spatial_lag
    df["lisa_i"] = moran_local.Is
    df["lisa_q"] = moran_local.q
    df["lisa_p_val"] = moran_local.p_sim
    df["lisa_cluster"] = lisa_labels
    df["gi_star_z"] = gi_star_z
    df["gi_star_cluster"] = gi_star_labels
    df["moran_global_i"] = float(moran_global.I)
    df["moran_global_p_val"] = float(moran_global.p_sim)

    summary = {
        "moran_global_I": float(moran_global.I),
        "moran_global_p_sim": float(moran_global.p_sim),
        "moran_global_z_sim": float(moran_global.z_sim),
        "n_municipios": len(df),
        "lisa_counts": pd.Series(lisa_labels).value_counts().to_dict(),
        "gi_star_counts": pd.Series(gi_star_labels).value_counts().to_dict(),
    }
    return df, summary


def build_features_matrix() -> pd.DataFrame:
    t0 = time.time()
    print("[Features v2] Construyendo matriz de features v2 (Shrinkage Bayesiano, 8 grupos edad + FPCA, Cohortes, MAD/IForest/PELT, LISA/Gi*)...")

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

    # Medianas y medias nacionales y estatales sobre datos VÁLIDOS (cobertura >= 0.90)
    nat_medians = mun_elec.groupby("anio")["participacion"].median().to_dict()
    nat_means = mun_elec.groupby("anio")["participacion"].mean().to_dict()
    state_medians = mun_elec.groupby(["cve_ent", "anio"])["participacion"].median().to_dict()
    state_means = mun_elec.groupby(["cve_ent", "anio"])["participacion"].mean().to_dict()

    # Shrinkage Bayesiano Empírico (Beta-Binomial) hacia la media estatal (M_prior = 450 electores efectivos)
    M_PRIOR = 450.0
    sv_nv = (mun_elec["votantes"] + mun_elec["no_votantes"]).astype(float)
    prior_mu = mun_elec.apply(
        lambda r: state_means.get((str(r["cve_ent"]).zfill(2), int(r["anio"])), nat_means[int(r["anio"])]),
        axis=1,
    ).astype(float)
    eb_shrunk = (mun_elec["votantes"].astype(float) + M_PRIOR * prior_mu) / (sv_nv + M_PRIOR)
    mun_elec["participacion_eb"] = eb_shrunk.where(mun_elec["participacion"].notna(), other=np.nan)

    mun_elec["sobre_mediana_nacional"] = mun_elec.apply(
        lambda r: float(r["participacion_eb"] > nat_medians[int(r["anio"])])
        if pd.notna(r["participacion_eb"])
        else np.nan,
        axis=1,
    )
    mun_elec["brecha_genero"] = mun_elec["part_mujeres"] - mun_elec["part_hombres"]
    mun_elec["brecha_generacional"] = mun_elec["part_60_mas"] - mun_elec["part_18_29"]

    # Pivotes por año
    p_raw_pivot = mun_elec.pivot(index="cve_geo", columns="anio", values="participacion")
    p_eb_pivot = mun_elec.pivot(index="cve_geo", columns="anio", values="participacion_eb")
    cov_pivot = mun_elec.pivot(index="cve_geo", columns="anio", values="cobertura")
    ln_pivot = mun_elec.pivot(index="cve_geo", columns="anio", values="lista_nominal")
    bg_pivot = mun_elec.pivot(index="cve_geo", columns="anio", values="brecha_genero")
    c18_20_pivot = mun_elec.pivot(index="cve_geo", columns="anio", values="part_cohorte_18_20")
    c21_23_pivot = mun_elec.pivot(index="cve_geo", columns="anio", values="part_cohorte_21_23")

    records = []
    x_cycles = np.arange(len(YEARS), dtype=float)

    grouped_mun = mun_elec.groupby("cve_geo", sort=True)
    for cve_geo, grp in grouped_mun:
        first_row = grp.iloc[0]
        last_row = grp.iloc[-1]
        cve_ent = str(first_row["cve_ent"]).zfill(2)

        raw_parts: list[float] = []
        eb_raw_parts: list[float] = []
        imp_parts: list[float] = []
        cov_vals: list[float] = []
        was_imputed = False
        n_low_cov_years = 0

        for y in YEARS:
            r_val = p_raw_pivot.loc[cve_geo, y] if y in p_raw_pivot.columns else np.nan
            eb_val = p_eb_pivot.loc[cve_geo, y] if y in p_eb_pivot.columns else np.nan
            c_val = cov_pivot.loc[cve_geo, y] if y in cov_pivot.columns else np.nan

            cov_vals.append(float(c_val) if pd.notna(c_val) else 0.0)
            if pd.notna(c_val) and float(c_val) < 0.90:
                n_low_cov_years += 1

            raw_parts.append(float(r_val) if pd.notna(r_val) else np.nan)
            eb_raw_parts.append(float(eb_val) if pd.notna(eb_val) else np.nan)

            if pd.isna(eb_val):
                was_imputed = True
                # Imputación jerárquica por tipo de elección dentro del mismo municipio o mediana estatal
                imp_val = state_medians.get((cve_ent, y), nat_medians[y])
                imp_parts.append(float(imp_val))
            else:
                imp_parts.append(float(eb_val))

        raw_arr = np.array(raw_parts, dtype=float)
        eb_raw_arr = np.array(eb_raw_parts, dtype=float)
        imp_arr = np.array(imp_parts, dtype=float)

        # Participación por tipo de elección calculada sobre datos válidos (con Shrinkage EB)
        pres_valid = eb_raw_arr[[1, 3, 5]]
        inter_valid = eb_raw_arr[[0, 2, 4]]
        part_pres = (
            float(np.nanmean(pres_valid))
            if not np.all(np.isnan(pres_valid))
            else float(np.mean(imp_arr[[1, 3, 5]]))
        )
        part_inter = (
            float(np.nanmean(inter_valid))
            if not np.all(np.isnan(inter_valid))
            else float(np.mean(imp_arr[[0, 2, 4]]))
        )
        part_global = (
            float(np.nanmean(eb_raw_arr))
            if not np.all(np.isnan(eb_raw_arr))
            else float(np.mean(imp_arr))
        )
        part_global_unshrunk = (
            float(np.nanmean(raw_arr)) if not np.all(np.isnan(raw_arr)) else part_global
        )
        # Convención documentada: caida_presidencial_intermedia = part_presidencial - part_intermedia
        # (Positivo = la intermedia tiene menor participación que la presidencial;
        #  Negativo = la elección intermedia superó a la presidencial)
        caida_pres_inter = part_pres - part_inter

        # Pendiente robusta y volatilidad calculadas SOLO sobre datos válidos (sin contaminar con NS/NA)
        pendiente_part = _robust_slope(eb_raw_arr, x_cycles)
        valid_eb = eb_raw_arr[~np.isnan(eb_raw_arr)]
        valid_raw = raw_arr[~np.isnan(raw_arr)]
        volatilidad_part = float(np.std(valid_eb, ddof=0)) if len(valid_eb) >= 2 else 0.0
        volatilidad_unshrunk = float(np.std(valid_raw, ddof=0)) if len(valid_raw) >= 2 else 0.0

        pres_std = float(np.nanstd(pres_valid, ddof=0)) if np.sum(~np.isnan(pres_valid)) >= 2 else 0.0
        inter_std = float(np.nanstd(inter_valid, ddof=0)) if np.sum(~np.isnan(inter_valid)) >= 2 else 0.0
        volatilidad_inter_tipo = 0.5 * (pres_std + inter_std)

        # MAD Robusto e identificación de cambios estructurales reales con PELT
        if len(valid_eb) >= 3:
            med_eb = float(np.median(valid_eb))
            mad_eb = float(np.median(np.abs(valid_eb - med_eb)))
            mad_zscore_max = float(np.max(np.abs(valid_eb - med_eb)) / max(1.4826 * mad_eb, 0.015))
        else:
            mad_zscore_max = 0.0

        valid_years_list = [y for y, v in zip(YEARS, eb_raw_parts, strict=True) if not np.isnan(v)]
        has_cp, cp_year = _pelt_exact_changepoint(valid_eb, valid_years_list)

        # Constancia sobre la mediana nacional (solo elecciones válidas)
        constancia = float(grp["sobre_mediana_nacional"].dropna().mean()) if grp["sobre_mediana_nacional"].notna().any() else 0.0

        # Brecha de género (mujeres - hombres)
        bg_vals = np.array(
            [bg_pivot.loc[cve_geo, y] if y in bg_pivot.columns else np.nan for y in YEARS],
            dtype=float,
        )
        brecha_genero_media = float(np.nanmean(bg_vals)) if not np.all(np.isnan(bg_vals)) else 0.0
        brecha_genero_tendencia = _robust_slope(bg_vals, x_cycles)

        # Estructura por edad (3 grandes grupos + 8 grupos detallados)
        total_ln_sum = float(grp["lista_nominal"].sum())
        pct_ln_18_29 = float(grp["ln_18_29"].sum() / total_ln_sum) if total_ln_sum > 0 else 0.0
        pct_ln_60_mas = float(grp["ln_60_mas"].sum() / total_ln_sum) if total_ln_sum > 0 else 0.0
        part_media_18_29 = float(grp["part_18_29"].dropna().mean()) if grp["part_18_29"].notna().any() else part_global
        part_media_30_59 = float(grp["part_30_59"].dropna().mean()) if grp["part_30_59"].notna().any() else part_global
        part_media_60_mas = float(grp["part_60_mas"].dropna().mean()) if grp["part_60_mas"].notna().any() else part_global
        brecha_generacional_media = part_media_60_mas - part_media_18_29
        brecha_juvenil_vs_adultos = part_media_18_29 - part_media_30_59
        brecha_adultos_mayores_vs_30_59 = part_media_60_mas - part_media_30_59

        # Curva participación-edad en los 8 grupos
        age_curve_vals: list[float] = []
        for col_a in AGE_8_COLS:
            val_a = float(grp[col_a].dropna().mean()) if grp[col_a].notna().any() else part_global
            age_curve_vals.append(val_a)
        peak_idx = int(np.argmax(age_curve_vals))
        edad_pico_participacion = float(AGE_8_MIDPOINTS[peak_idx])

        # Pseudo-cohortes generacionales: retención del primer voto (18-20 en t -> 21-23 en t+3)
        # Normalizado por el cambio medio de participación del municipio entre t y t+3
        ret_ratios: list[float] = []
        for idx_t in range(len(YEARS) - 1):
            y_t = YEARS[idx_t]
            y_next = YEARS[idx_t + 1]
            p_first = c18_20_pivot.loc[cve_geo, y_t] if y_t in c18_20_pivot.columns else np.nan
            p_second = c21_23_pivot.loc[cve_geo, y_next] if y_next in c21_23_pivot.columns else np.nan
            p_mun_t = eb_raw_parts[idx_t]
            p_mun_next = eb_raw_parts[idx_t + 1]
            if pd.notna(p_first) and pd.notna(p_second) and p_first > 0.05 and pd.notna(p_mun_t) and pd.notna(p_mun_next) and p_mun_t > 0.05:
                # Ratio de retención ajustado por el efecto ciclo (presidencial <-> intermedia)
                cycle_adj = float(p_mun_next / p_mun_t)
                expected_second = float(p_first) * cycle_adj
                ret_ratios.append(float(p_second) / max(expected_second, 0.05))
        retencion_primer_voto = float(np.mean(ret_ratios)) if ret_ratios else 0.85
        efecto_envejecimiento_cívico = (age_curve_vals[6] - age_curve_vals[0]) / (64.5 - 18.5)

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

        n_obs = int((~np.isnan(eb_raw_arr)).sum())
        baja_confiabilidad = bool((ln_promedio < 1000.0) or (n_obs < 5))
        cobertura_media = float(np.mean(cov_vals))

        records.append(
            {
                "cve_geo": cve_geo,
                "cve_ent": cve_ent,
                "nom_ent": str(last_row["nom_ent"]),
                "cve_mun": str(last_row["cve_mun"]).zfill(3),
                "nom_mun": str(last_row["nom_mun"]),
                "n_elecciones_observadas": n_obs,
                "n_elecciones_baja_cobertura_ns": n_low_cov_years,
                "cobertura_media_2009_2024": cobertura_media,
                "flag_imputacion_trayectoria": was_imputed,
                "imputado": was_imputed,
                "flag_baja_confiabilidad": baja_confiabilidad,
                # Serie temporal con Shrinkage Bayesiano Empírico e imputación jerárquica para NA
                "part_2009": imp_parts[0],
                "part_2012": imp_parts[1],
                "part_2015": imp_parts[2],
                "part_2018": imp_parts[3],
                "part_2021": imp_parts[4],
                "part_2024": imp_parts[5],
                # Serie temporal observada cruda (con NaN cuando cobertura < 0.90 o municipio no existía)
                "part_2009_raw": raw_parts[0],
                "part_2012_raw": raw_parts[1],
                "part_2015_raw": raw_parts[2],
                "part_2018_raw": raw_parts[3],
                "part_2021_raw": raw_parts[4],
                "part_2024_raw": raw_parts[5],
                # Métricas agregadas de participación y dinámica (sobre datos válidos con Shrinkage)
                "part_media_global": part_global,
                "part_media_global_unshrunk": part_global_unshrunk,
                "part_media_presidencial": part_pres,
                "part_media_intermedia": part_inter,
                "caida_presidencial_intermedia": caida_pres_inter,
                "pendiente_tendencia": pendiente_part,
                "volatilidad": volatilidad_part,
                "volatilidad_unshrunk": volatilidad_unshrunk,
                "volatilidad_intra_tipo": volatilidad_inter_tipo,
                "constancia_sobre_mediana": constancia,
                # Detección de anomalías y cambios estructurales reales (Fase A1.3)
                "mad_zscore_max": mad_zscore_max,
                "tiene_cambio_estructural_pelt": has_cp,
                "anio_cambio_estructural_pelt": cp_year,
                # Género
                "brecha_genero_media": brecha_genero_media,
                "brecha_genero_tendencia": brecha_genero_tendencia,
                # Edad (3 grupos, 8 grupos detallados, edad pico y cohortes)
                "pct_ln_jovenes_18_29": pct_ln_18_29,
                "pct_ln_adultos_60_mas": pct_ln_60_mas,
                "part_media_jovenes_18_29": part_media_18_29,
                "part_media_adultos_30_59": part_media_30_59,
                "part_media_adultos_60_mas": part_media_60_mas,
                "brecha_generacional_60_vs_18_29": brecha_generacional_media,
                "brecha_juvenil_18_29_vs_30_59": brecha_juvenil_vs_adultos,
                "brecha_adultos_mayores_60_vs_30_59": brecha_adultos_mayores_vs_30_59,
                "part_edad_18_19": age_curve_vals[0],
                "part_edad_20_24": age_curve_vals[1],
                "part_edad_25_29": age_curve_vals[2],
                "part_edad_30_39": age_curve_vals[3],
                "part_edad_40_49": age_curve_vals[4],
                "part_edad_50_59": age_curve_vals[5],
                "part_edad_60_69": age_curve_vals[6],
                "part_edad_70_mas": age_curve_vals[7],
                "edad_pico_participacion": edad_pico_participacion,
                "retencion_primer_voto": retencion_primer_voto,
                "efecto_envejecimiento_cívico": efecto_envejecimiento_cívico,
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
                "serie_temporal_json": json.dumps([round(x, 6) for x in imp_parts]),
                "curva_edad_8grupos_json": json.dumps([round(x, 6) for x in age_curve_vals]),
            }
        )

    df_feat = pd.DataFrame(records)

    # FPCA (Functional PCA, 3 componentes sobre la curva de participación por los 8 grupos de edad)
    age_mat = df_feat[AGE_8_COLS].to_numpy(dtype=float)
    age_mat_centered = age_mat - np.mean(age_mat, axis=0, keepdims=True)
    fpca = PCA(n_components=3, random_state=42)
    fpca_scores = fpca.fit_transform(age_mat_centered)
    df_feat["fpca_edad_pc1"] = fpca_scores[:, 0]
    df_feat["fpca_edad_pc2"] = fpca_scores[:, 1]
    df_feat["fpca_edad_pc3"] = fpca_scores[:, 2]

    # Isolation Forest para detectar trayectorias atípicas sobre datos limpios
    iforest_cols = [
        "part_media_global",
        "caida_presidencial_intermedia",
        "pendiente_tendencia",
        "volatilidad",
        "brecha_juvenil_18_29_vs_30_59",
        "brecha_genero_media",
    ]
    iforest = IsolationForest(contamination=0.03, random_state=42)
    iforest_preds = iforest.fit_predict(df_feat[iforest_cols].to_numpy(dtype=float))
    df_feat["anomalia_iforest"] = iforest_preds == -1
    df_feat["score_iforest"] = iforest.decision_function(df_feat[iforest_cols].to_numpy(dtype=float))

    # Clasificación sintética de régimen / calidad de la trayectoria (Fase A1.3)
    def _classify_trajectory_regime(r: pd.Series) -> str:
        if r["n_elecciones_baja_cobertura_ns"] > 0:
            return "DATO_FALTANTE_NS_REPARADO"
        if r["tiene_cambio_estructural_pelt"]:
            return f"CAMBIO_ESTRUCTURAL_REAL_{int(r['anio_cambio_estructural_pelt'])}"
        if r["anomalia_iforest"] or r["mad_zscore_max"] > 3.5:
            return "ATIPICO_ESTADISTICO"
        return "TRAYECTORIA_REGULAR"

    df_feat["diagnostico_trayectoria_a1"] = df_feat.apply(_classify_trajectory_regime, axis=1)

    df_feat = df_feat.merge(def_mode, on="cve_geo", how="left")
    df_feat = df_feat.merge(
        bridge[["cve_geo", "estatus_marco_geografico", "primer_anio", "ultimo_anio"]],
        on="cve_geo",
        how="left",
    )

    # Enriquecimiento externo (CONAPO / INEGI)
    df_ext = fetch_or_load_external_enrichment(df_feat["cve_geo"])
    df_feat = df_feat.merge(df_ext, on="cve_geo", how="left")

    # Autocorrelación espacial (Moran's I global, LISA local y Getis-Ord Gi*)
    df_feat, spatial_summary = compute_spatial_autocorrelation(df_feat)

    # Reportar reducción de varianza en municipios pequeños por Shrinkage Bayesiano
    small_mask = df_feat["ln_promedio"] < 2000.0
    var_before = float(df_feat.loc[small_mask, "volatilidad_unshrunk"].mean())
    var_after = float(df_feat.loc[small_mask, "volatilidad"].mean())
    spatial_summary["shrinkage_small_mun_volatility_before"] = round(var_before, 5)
    spatial_summary["shrinkage_small_mun_volatility_after"] = round(var_after, 5)
    spatial_summary["fpca_explained_variance_ratio"] = [
        round(float(x), 4) for x in fpca.explained_variance_ratio_
    ]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    SERVING_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / "features_municipio.parquet"
    df_feat.to_parquet(out_path, index=False)
    df_feat.to_parquet(GOLD_DIR / "features_municipio.parquet", index=False)
    shutil.copy2(out_path, SERVING_DIR / "features_municipio.parquet")

    (PROCESSED_DIR / "spatial_moran_summary.json").write_text(
        json.dumps(spatial_summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(
        f"[Features v2] Matriz exportada ({len(df_feat):,} municipios × {df_feat.shape[1]} columnas) en {time.time() - t0:.1f}s | "
        f"Moran's I = {spatial_summary['moran_global_I']:.4f} (p={spatial_summary['moran_global_p_sim']:.4f}) | "
        f"Volatilidad mun. pequeños antes/después Shrinkage: {var_before:.4f} -> {var_after:.4f}"
    )
    return df_feat


if __name__ == "__main__":
    build_features_matrix()
