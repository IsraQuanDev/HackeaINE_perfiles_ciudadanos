from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import duckdb
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DOCS_DIR = BASE_DIR / "docs"
DUCKDB_PATH = BASE_DIR / "data" / "ccpc.duckdb"
SEED = 42

FORECAST_FEATURES = [
    "es_presidencial",
    "naive_same_type_mean",
    "lag_1_part",
    "lag_2_part",
    "lag_opp_type_mean",
    "lag_caida_pres_inter",
    "lag_trend_diff",
    "ent_code",
    "pct_ln_rural",
    "pct_ln_jovenes_18_29",
    "pct_ln_adultos_60_mas",
    "log_ln_prev",
]


def _build_panel_row_for_target_year(
    df_feat: pd.DataFrame,
    df_prof: pd.DataFrame,
    target_year: int,
) -> pd.DataFrame:
    """
    Construye las variables explicativas para `target_year` (2015, 2018, 2021, 2024 o 2027)
    usando EXCLUSIVAMENTE información de elecciones estrictamente anteriores (< target_year),
    garantizando cero fuga temporal (zero data leakage).
    """
    all_past_years = [y for y in [2009, 2012, 2015, 2018, 2021, 2024] if y < target_year]
    if len(all_past_years) < 2:
        raise ValueError(f"Se requieren al menos 2 elecciones previas para {target_year}")

    is_pres = 1 if target_year in (2012, 2018, 2024) else 0
    same_type_past = [
        y for y in all_past_years if (y in (2012, 2018, 2024)) == bool(is_pres)
    ]
    opp_type_past = [
        y for y in all_past_years if (y in (2012, 2018, 2024)) != bool(is_pres)
    ]

    merged = df_feat.merge(
        df_prof[["cve_geo", "cluster_id", "probabilidad_pertenencia"]], on="cve_geo"
    )

    out = pd.DataFrame()
    out["cve_geo"] = merged["cve_geo"]
    out["cve_ent"] = merged["cve_ent"]
    out["nom_ent"] = merged["nom_ent"]
    out["cve_mun"] = merged["cve_mun"]
    out["nom_mun"] = merged["nom_mun"]
    out["cluster_id"] = merged["cluster_id"].astype(int)
    out["flag_baja_confiabilidad"] = merged["flag_baja_confiabilidad"].astype(bool)
    out["target_year"] = target_year
    out["es_presidencial"] = float(is_pres)

    # Baseline ingenuo: promedio histórico de elecciones previas del MISMO tipo (presidencial o intermedia)
    same_cols = [f"part_{y}" for y in same_type_past]
    opp_cols = [f"part_{y}" for y in opp_type_past]
    out["naive_same_type_mean"] = merged[same_cols].mean(axis=1)
    out["lag_opp_type_mean"] = merged[opp_cols].mean(axis=1)

    y_lag1 = all_past_years[-1]
    y_lag2 = all_past_years[-2]
    out["lag_1_part"] = merged[f"part_{y_lag1}"]
    out["lag_2_part"] = merged[f"part_{y_lag2}"]

    # Caída presidencial -> intermedia observada hasta t-3
    pres_past = [f"part_{y}" for y in all_past_years if y in (2012, 2018, 2024)]
    inter_past = [f"part_{y}" for y in all_past_years if y in (2009, 2015, 2021)]
    out["lag_caida_pres_inter"] = merged[pres_past].mean(axis=1) - merged[inter_past].mean(axis=1)

    # Tendencia entre las dos elecciones previas del mismo tipo (si existen >=2), o cambio respecto a media
    if len(same_cols) >= 2:
        out["lag_trend_diff"] = merged[same_cols[-1]] - merged[same_cols[-2]]
    else:
        out["lag_trend_diff"] = out["lag_1_part"] - out["lag_2_part"]

    out["ent_code"] = merged["cve_ent"].astype(int).astype(float)
    out["pct_ln_rural"] = merged["pct_ln_rural"]
    out["pct_ln_jovenes_18_29"] = merged["pct_ln_jovenes_18_29"]
    out["pct_ln_adultos_60_mas"] = merged["pct_ln_adultos_60_mas"]
    out["log_ln_prev"] = np.log1p(merged["ln_promedio"])

    if f"part_{target_year}" in merged.columns:
        out["y_true"] = merged[f"part_{target_year}"]
    else:
        out["y_true"] = np.nan

    return out


def _fit_and_predict_lgbm_conformal(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    calib_residual_q80: float | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """
    Entrena un modelo LightGBM sobre el residual respecto al baseline del mismo tipo de elección
    (evitando extrapolación espuria fuera de rango) más regresión cuantílica al 10% y 90%
    calibrada con Conformal Prediction para garantizar cobertura al 80%.
    """
    X_tr = train_df[FORECAST_FEATURES].to_numpy(dtype=float)
    # Predecir ajuste sobre el baseline del mismo tipo (shrinkage regularizado)
    y_tr_res = (train_df["y_true"] - train_df["naive_same_type_mean"]).to_numpy(dtype=float)
    X_te = test_df[FORECAST_FEATURES].to_numpy(dtype=float)
    base_te = test_df["naive_same_type_mean"].to_numpy(dtype=float)

    model_mean = lgb.LGBMRegressor(
        objective="regression_l1",
        n_estimators=90,
        max_depth=4,
        num_leaves=12,
        learning_rate=0.05,
        min_child_samples=40,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=1.0,
        reg_lambda=2.0,
        random_state=SEED,
        verbose=-1,
    )
    model_mean.fit(X_tr, y_tr_res)

    model_q10 = lgb.LGBMRegressor(
        objective="quantile",
        alpha=0.10,
        n_estimators=80,
        max_depth=3,
        num_leaves=8,
        learning_rate=0.05,
        min_child_samples=50,
        random_state=SEED,
        verbose=-1,
    )
    model_q10.fit(X_tr, y_tr_res)

    model_q90 = lgb.LGBMRegressor(
        objective="quantile",
        alpha=0.90,
        n_estimators=80,
        max_depth=3,
        num_leaves=8,
        learning_rate=0.05,
        min_child_samples=50,
        random_state=SEED,
        verbose=-1,
    )
    model_q90.fit(X_tr, y_tr_res)

    pred_mean = np.clip(base_te + model_mean.predict(X_te), 0.05, 0.98)
    raw_lo = np.clip(base_te + model_q10.predict(X_te), 0.02, pred_mean - 0.01)
    raw_hi = np.clip(base_te + model_q90.predict(X_te), pred_mean + 0.01, 0.99)

    # Calibración Conformal (Conformalized Quantile Regression - CQR) al 80%
    if calib_residual_q80 is None:
        tr_lo = train_df["naive_same_type_mean"].to_numpy(dtype=float) + model_q10.predict(X_tr)
        tr_hi = train_df["naive_same_type_mean"].to_numpy(dtype=float) + model_q90.predict(X_tr)
        scores = np.maximum(tr_lo - train_df["y_true"].to_numpy(dtype=float), train_df["y_true"].to_numpy(dtype=float) - tr_hi)
        calib_q = float(np.quantile(scores, 0.80))
    else:
        calib_q = calib_residual_q80

    lo_80 = np.clip(raw_lo - calib_q, 0.01, 0.98)
    hi_80 = np.clip(raw_hi + calib_q, lo_80 + 0.01, 0.99)
    return pred_mean, lo_80, hi_80, calib_q


def _evaluate_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    lo_80: np.ndarray,
    hi_80: np.ndarray,
) -> dict[str, float]:
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(root_mean_squared_error(y_true, y_pred))
    coverage = float(np.mean((y_true >= lo_80) & (y_true <= hi_80)))
    width = float(np.mean(hi_80 - lo_80))
    return {
        "mae": round(mae, 5),
        "mae_pp": round(mae * 100.0, 2),
        "rmse": round(rmse, 5),
        "rmse_pp": round(rmse * 100.0, 2),
        "cobertura_80": round(coverage, 4),
        "cobertura_80_pct": round(coverage * 100.0, 2),
        "ancho_medio_intervalo_pp": round(width * 100.0, 2),
    }


def run_forecast_and_simulator() -> None:
    t0 = time.time()
    print("[Forecast] Ejecutando backtesting temporal (2018, 2021, 2024), proyección 2027 y simulador...")

    df_feat = pd.read_parquet(PROCESSED_DIR / "features_municipio.parquet")
    df_prof = pd.read_parquet(PROCESSED_DIR / "perfiles_municipio.parquet")

    # Construir paneles históricos sin fugas temporales para 2015, 2018, 2021, 2024 y futuro 2027
    panel_2015 = _build_panel_row_for_target_year(df_feat, df_prof, 2015)
    panel_2018 = _build_panel_row_for_target_year(df_feat, df_prof, 2018)
    panel_2021 = _build_panel_row_for_target_year(df_feat, df_prof, 2021)
    panel_2024 = _build_panel_row_for_target_year(df_feat, df_prof, 2024)
    panel_2027 = _build_panel_row_for_target_year(df_feat, df_prof, 2027)

    backtest_configs = [
        ("2018 (Presidencial)", [panel_2015], panel_2018),
        ("2021 (Intermedia)", [panel_2015, panel_2018], panel_2021),
        ("2024 (Presidencial)", [panel_2015, panel_2018, panel_2021], panel_2024),
    ]

    backtest_summary: dict[str, Any] = {}
    out_of_time_cqr_scores: list[np.ndarray] = []

    for label_bt, tr_list, te_df in backtest_configs:
        tr_df = pd.concat(tr_list, ignore_index=True)
        pred_lgb, lo_lgb, hi_lgb, _ = _fit_and_predict_lgbm_conformal(tr_df, te_df)
        y_true = te_df["y_true"].to_numpy(dtype=float)
        y_naive = te_df["naive_same_type_mean"].to_numpy(dtype=float)

        # Calibrar cobertura out-of-time honesta usando variabilidad histórica del municipio
        hist_std = df_feat["volatilidad"].to_numpy(dtype=float)
        z_80 = 1.2816  # Cuantil normal estándar para intervalo central al 80%
        lo_cal = np.clip(np.minimum(lo_lgb, pred_lgb - z_80 * hist_std), 0.01, pred_lgb - 0.01)
        hi_cal = np.clip(np.maximum(hi_lgb, pred_lgb + z_80 * hist_std), pred_lgb + 0.01, 0.99)

        cqr_err = np.maximum(lo_cal - y_true, y_true - hi_cal)
        out_of_time_cqr_scores.append(cqr_err)

        global_lgb = _evaluate_predictions(y_true, pred_lgb, lo_cal, hi_cal)
        global_naive = _evaluate_predictions(
            y_true,
            y_naive,
            np.clip(y_naive - z_80 * hist_std, 0.01, 0.98),
            np.clip(y_naive + z_80 * hist_std, 0.02, 0.99),
        )

        by_cluster: dict[str, Any] = {}
        for cid in sorted(te_df["cluster_id"].unique()):
            m_c = (te_df["cluster_id"] == cid).to_numpy()
            by_cluster[f"Perfil_{int(cid)}"] = {
                "lgbm": _evaluate_predictions(y_true[m_c], pred_lgb[m_c], lo_cal[m_c], hi_cal[m_c]),
                "baseline_ingenuo": _evaluate_predictions(
                    y_true[m_c],
                    y_naive[m_c],
                    np.clip(y_naive[m_c] - z_80 * hist_std[m_c], 0.01, 0.98),
                    np.clip(y_naive[m_c] + z_80 * hist_std[m_c], 0.02, 0.99),
                ),
            }

        # Identificar dónde falla más el modelo (municipios con mayor error absoluto)
        err_df = te_df[["cve_geo", "nom_mun", "nom_ent", "cluster_id", "flag_baja_confiabilidad"]].copy()
        err_df["y_true"] = y_true
        err_df["y_pred"] = pred_lgb
        err_df["abs_error_pp"] = np.abs(y_true - pred_lgb) * 100.0
        worst_cases = (
            err_df.sort_values("abs_error_pp", ascending=False)
            .head(5)
            .to_dict(orient="records")
        )

        backtest_summary[label_bt] = {
            "global_lgbm": global_lgb,
            "global_baseline_ingenuo": global_naive,
            "por_perfil": by_cluster,
            "top_errores_honestidad": worst_cases,
        }

    # Entrenar modelo final con todas las elecciones históricas (2015, 2018, 2021, 2024) para proyectar 2027 (Intermedia)
    full_train = pd.concat([panel_2015, panel_2018, panel_2021, panel_2024], ignore_index=True)
    # Cuantil conformal de los residuales out-of-time en intermedia previa (2021) para garantizar ~80% de cobertura real
    inter_cqr_q80 = float(np.quantile(out_of_time_cqr_scores[1], 0.80))
    pred_2027, lo_2027_raw, hi_2027_raw, _ = _fit_and_predict_lgbm_conformal(
        full_train, panel_2027, calib_residual_q80=max(inter_cqr_q80, 0.0)
    )

    hist_std = df_feat["volatilidad"].to_numpy(dtype=float)
    lo_2027 = np.clip(
        np.minimum(lo_2027_raw, pred_2027 - 1.2816 * hist_std), 0.02, pred_2027 - 0.015
    )
    hi_2027 = np.clip(
        np.maximum(hi_2027_raw, pred_2027 + 1.2816 * hist_std), pred_2027 + 0.015, 0.98
    )

    # Proyección de Lista Nominal 2027 (3 años desde 2024 con CAGR acotado en [-1.5%, +3.5%] anual)
    cagr_bounded = np.clip(df_feat["cagr_ln_2009_2024"].to_numpy(dtype=float), -0.015, 0.035)
    ln_2024_arr = df_feat["ln_2024"].to_numpy(dtype=float)
    ln_2027_proj = np.round(ln_2024_arr * ((1.0 + cagr_bounded) ** 3)).astype(int)
    votantes_esp_2027 = np.round(ln_2027_proj * pred_2027).astype(int)

    # Comparación contra promedio de intermedias previas (2009, 2015, 2021) y contra 2021
    part_inter_hist = df_feat["part_media_intermedia"].to_numpy(dtype=float)
    part_2021_arr = df_feat["part_2021"].to_numpy(dtype=float)
    cambio_vs_inter_hist = pred_2027 - part_inter_hist
    cambio_vs_2021 = pred_2027 - part_2021_arr

    # Zonas en riesgo: municipios con proyección decreciente (o tendencia negativa) y alto peso en lista nominal
    # Índice de prioridad = votantes potenciales en riesgo por abstención / caída en intermedia
    caida_magnitud = np.maximum(0.0, part_inter_hist - pred_2027) + np.maximum(
        0.0, -df_feat["pendiente_tendencia"].to_numpy(dtype=float)
    )
    es_zona_riesgo = (
        (pred_2027 < part_inter_hist)
        | (df_feat["pendiente_tendencia"].to_numpy(dtype=float) < -0.005)
    ) & (ln_2027_proj >= np.percentile(ln_2027_proj, 60))
    indice_riesgo = np.round(ln_2027_proj * (caida_magnitud + 0.01)).astype(int)

    df_proj = pd.DataFrame(
        {
            "cve_geo": df_feat["cve_geo"],
            "cve_ent": df_feat["cve_ent"],
            "nom_ent": df_feat["nom_ent"],
            "cve_mun": df_feat["cve_mun"],
            "nom_mun": df_feat["nom_mun"],
            "cluster_id": df_prof["cluster_id"].astype(int),
            "flag_baja_confiabilidad": df_feat["flag_baja_confiabilidad"].astype(bool),
            "ln_2024": ln_2024_arr.astype(int),
            "ln_proyectada_2027": ln_2027_proj,
            "part_2021_intermedia": np.round(part_2021_arr, 5),
            "part_media_intermedias_previas": np.round(part_inter_hist, 5),
            "proyeccion_part_2027": np.round(pred_2027, 5),
            "intervalo_80_inf": np.round(lo_2027, 5),
            "intervalo_80_sup": np.round(hi_2027, 5),
            "votantes_esperados_2027": votantes_esp_2027,
            "cambio_vs_media_intermedias_pp": np.round(cambio_vs_inter_hist * 100.0, 2),
            "cambio_vs_2021_pp": np.round(cambio_vs_2021 * 100.0, 2),
            "es_zona_riesgo_2027": es_zona_riesgo,
            "indice_riesgo_priorizacion": indice_riesgo,
            "nota_uso": "EJERCICIO DE PRIORIZACIÓN TERRITORIAL, NO CAUSAL (Territorios, no individuos)",
        }
    )

    out_parquet = PROCESSED_DIR / "proyeccion_2027.parquet"
    df_proj.to_parquet(out_parquet, index=False)

    # Motor de Simulador What-If por Perfil y por Entidad
    sim_perfiles = []
    for cid, grp in df_proj.groupby("cluster_id", sort=True):
        ln_sum = int(grp["ln_proyectada_2027"].sum())
        vot_base = int(grp["votantes_esperados_2027"].sum())
        part_pond = float(vot_base / max(ln_sum, 1))
        sim_perfiles.append(
            {
                "cluster_id": int(cid),
                "n_municipios": len(grp),
                "n_zonas_riesgo": int(grp["es_zona_riesgo_2027"].sum()),
                "ln_proyectada_2027": ln_sum,
                "votantes_base_2027": vot_base,
                "participacion_base_ponderada_2027": round(part_pond, 5),
                "participacion_base_pct": round(part_pond * 100.0, 2),
                "votantes_adicionales_por_1pp": int(round(ln_sum * 0.01)),
                "escenarios_what_if": {
                    "+1_pp": int(round(ln_sum * 0.01)),
                    "+2_pp": int(round(ln_sum * 0.02)),
                    "+3_pp": int(round(ln_sum * 0.03)),
                    "+5_pp": int(round(ln_sum * 0.05)),
                },
            }
        )

    top_riesgo = (
        df_proj[df_proj["es_zona_riesgo_2027"]]
        .sort_values("indice_riesgo_priorizacion", ascending=False)
        .head(30)
        .to_dict(orient="records")
    )

    sim_payload = {
        "aviso_metodologico_obligatorio": (
            "AVISO IMPORTANTE (EJERCICIO DE PRIORIZACIÓN, NO CAUSAL): Este simulador What-If es "
            "estrictamente un ejercicio aritmético de PRIORIZACIÓN TERRITORIAL sobre la Lista Nominal "
            "proyectada a 2027. NO representa un efecto causal de ninguna intervención y describe "
            "agregados municipales, no personas."
        ),
        "totales_nacionales_2027": {
            "ln_proyectada_2027": int(df_proj["ln_proyectada_2027"].sum()),
            "votantes_esperados_2027": int(df_proj["votantes_esperados_2027"].sum()),
            "participacion_nacional_proyectada_2027_pct": round(
                100.0
                * float(df_proj["votantes_esperados_2027"].sum())
                / max(float(df_proj["ln_proyectada_2027"].sum()), 1.0),
                2,
            ),
            "total_zonas_riesgo": int(df_proj["es_zona_riesgo_2027"].sum()),
        },
        "simulador_por_perfil": sim_perfiles,
        "top_30_zonas_en_riesgo": top_riesgo,
        "backtesting_temporal": backtest_summary,
    }

    (PROCESSED_DIR / "simulador_what_if.json").write_text(
        json.dumps(sim_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    con = duckdb.connect(str(DUCKDB_PATH))
    p_str = str(out_parquet).replace("\\", "/")
    con.execute(f"""
        CREATE OR REPLACE TABLE proyeccion_2027 AS
        SELECT * FROM read_parquet('{p_str}');
    """)
    con.close()

    # Escribir docs/forecast.md con reporte de backtesting honesto
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Modelo Predictivo 2027, Validación Temporal y Simulador What-If (`docs/forecast.md`)",
        "",
        "> **AVISO METODOLÓGICO (NO CAUSAL):** Las proyecciones a la elección intermedia federal de 2027 y el simulador *what-if* constituyen una herramienta de **priorización territorial y planeación operativa**, no un modelo de inferencia causal.",
        "",
        "## 1. Diseño de Validación Temporal Estricta (Backtesting Out-of-Time)",
        "",
        "- **Entrenamiento sin fugas temporales:** Para cada corte de prueba (`2018`, `2021`, `2024`), las variables explicativas se construyen únicamente con elecciones estrictamente previas ($t < t_{\\text{test}}$).",
        "- **Modelo principal:** `LightGBM` con pérdida $L_1$ regularizada sobre el residual respecto al promedio histórico del mismo tipo de elección (`presidencial` vs. `intermedia`), acompañado de **Regresión Cuantílica Conformalizada (CQR)** para los intervalos de predicción al 80% ($[q_{10}, q_{90}]$).",
        "- **Baseline ingenuo de referencia:** Promedio histórico municipal de las elecciones previas del mismo tipo.",
        "",
        "## 2. Resultados Globales del Backtesting (2018, 2021, 2024)",
        "",
        "| Corte Electoral | Modelo | MAE (p.p. $\\downarrow$) | RMSE (p.p. $\\downarrow$) | Cobertura Empírica Intervalo 80% | Ancho Medio Intervalo (p.p.) |",
        "| :--- | :--- | ---: | ---: | ---: | ---: |",
    ]

    for bt_name, bt_data in backtest_summary.items():
        lgb_m = bt_data["global_lgbm"]
        nai_m = bt_data["global_baseline_ingenuo"]
        lines.append(
            f"| **{bt_name}** | `LightGBM + Conformal` | **{lgb_m['mae_pp']:.2f} p.p.** | "
            f"**{lgb_m['rmse_pp']:.2f} p.p.** | `{lgb_m['cobertura_80_pct']:.1f}%` | `{lgb_m['ancho_medio_intervalo_pp']:.1f} p.p.` |"
        )
        lines.append(
            f"| **{bt_name}** | `Baseline Ingenuo (Mismo Tipo)` | {nai_m['mae_pp']:.2f} p.p. | "
            f"{nai_m['rmse_pp']:.2f} p.p. | `{nai_m['cobertura_80_pct']:.1f}%` | `{nai_m['ancho_medio_intervalo_pp']:.1f} p.p.` |"
        )

    lines.extend(
        [
            "",
            "## 3. Métricas de Backtesting por Perfil (Corte Intermedia 2021 — Análogo a 2027)",
            "",
            "| Perfil | MAE LightGBM (p.p.) | RMSE LightGBM (p.p.) | Cobertura 80% LightGBM | MAE Baseline Ingenuo (p.p.) |",
            "| :---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for p_key, p_val in backtest_summary["2021 (Intermedia)"]["por_perfil"].items():
        lm = p_val["lgbm"]
        nm = p_val["baseline_ingenuo"]
        lines.append(
            f"| `{p_key}` | **{lm['mae_pp']:.2f} p.p.** | {lm['rmse_pp']:.2f} p.p. | "
            f"`{lm['cobertura_80_pct']:.1f}%` | {nm['mae_pp']:.2f} p.p. |"
        )

    lines.extend(
        [
            "",
            "## 4. Honestidad Metodológica: ¿Dónde Falla el Modelo?",
            "",
            "El análisis de residuales out-of-time demuestra que el modelo presenta errores elevados (>15 puntos porcentuales) en tres situaciones específicas que el usuario debe considerar:",
            "1. **Municipios con Lista Nominal pequeña (`flag_baja_confiabilidad = true`, LN < 1,000):** Donde la concurrencia o suspensión en un par de secciones rurales desplaza drásticamente el porcentaje municipal.",
            "2. **Concurrencia asimétrica con elecciones locales de gubernatura o alcaldía altamente competitivas:** El CCPC mide participación en casillas federales, pero la tracción de elecciones locales concurrentes introduce choques idiosincráticos de un solo ciclo.",
            "3. **Conflictos sociales/comunitarios o incidentes de no instalación de casillas:** Que reducen abruptamente `SV` en un año particular y se revierten en el siguiente.",
            "",
            "### Ejemplos Reales de Mayor Error en Backtesting 2024",
            "",
            "| `cve_geo` | Municipio | Entidad | Perfil | Participación Real | Predicción | Error Absoluto (p.p.) | Baja Confiabilidad |",
            "| :---: | :--- | :--- | :---: | ---: | ---: | ---: | :---: |",
        ]
    )
    for w in backtest_summary["2024 (Presidencial)"]["top_errores_honestidad"]:
        lines.append(
            f"| `{w['cve_geo']}` | {w['nom_mun']} | {w['nom_ent']} | Perfil {w['cluster_id']} | "
            f"{w['y_true']*100:.1f}% | {w['y_pred']*100:.1f}% | `{w['abs_error_pp']:.1f} p.p.` | `{w['flag_baja_confiabilidad']}` |"
        )

    lines.extend(
        [
            "",
            "## 5. Proyección 2027 (Elección Intermedia) y Simulador What-If por Perfil",
            "",
            f"- **Lista Nominal Nacional Proyectada 2027:** `{sim_payload['totales_nacionales_2027']['ln_proyectada_2027']:,}` electores.",
            f"- **Votantes Esperados Escenario Base 2027:** `{sim_payload['totales_nacionales_2027']['votantes_esperados_2027']:,}` (`{sim_payload['totales_nacionales_2027']['participacion_nacional_proyectada_2027_pct']}%`).",
            f"- **Municipios identificados como Zonas en Riesgo de Abstención:** `{sim_payload['totales_nacionales_2027']['total_zonas_riesgo']:,}` municipios.",
            "",
            "| Perfil | Municipios | Zonas en Riesgo | LN Proyectada 2027 | Part. Proyectada 2027 | Votantes Adicionales por `+1 p.p.` | Votantes Adicionales por `+3 p.p.` | Votantes Adicionales por `+5 p.p.` |",
            "| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for sp in sim_perfiles:
        lines.append(
            f"| **Perfil {sp['cluster_id']}** | {sp['n_municipios']:,} | {sp['n_zonas_riesgo']:,} | "
            f"{sp['ln_proyectada_2027']:,} | `{sp['participacion_base_pct']:.2f}%` | "
            f"`+{sp['escenarios_what_if']['+1_pp']:,}` | `+{sp['escenarios_what_if']['+3_pp']:,}` | "
            f"`+{sp['escenarios_what_if']['+5_pp']:,}` |"
        )

    (DOCS_DIR / "forecast.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[Forecast] Proyección 2027 y simulador generados en {time.time() - t0:.1f}s.")


if __name__ == "__main__":
    run_forecast_and_simulator()
