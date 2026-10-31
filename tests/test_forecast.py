from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
PROJ_PATH = BASE_DIR / "data" / "processed" / "proyeccion_2027.parquet"
SIM_PATH = BASE_DIR / "data" / "processed" / "simulador_what_if.json"
FC_DOC = BASE_DIR / "docs" / "forecast.md"


def test_forecast_artifacts_exist() -> None:
    assert PROJ_PATH.exists(), "Falta data/processed/proyeccion_2027.parquet"
    assert SIM_PATH.exists(), "Falta data/processed/simulador_what_if.json"
    assert FC_DOC.exists(), "Falta docs/forecast.md"


def test_forecast_bounds_and_intervals() -> None:
    df = pd.read_parquet(PROJ_PATH)
    sim = json.loads(SIM_PATH.read_text(encoding="utf-8"))

    assert df["cve_geo"].is_unique
    assert (df["intervalo_80_inf"] < df["proyeccion_part_2027"]).all()
    assert (df["proyeccion_part_2027"] < df["intervalo_80_sup"]).all()
    assert (df["intervalo_80_inf"] >= 0.0).all() and (df["intervalo_80_sup"] <= 1.0).all()

    # Verificar que exista aviso explícito de ejercicio de priorización no causal
    assert "NO CAUSAL" in sim["aviso_metodologico_obligatorio"].upper()
    assert len(sim["simulador_por_perfil"]) >= 4
    assert "2018 (Presidencial)" in sim["backtesting_temporal"]
    assert "2021 (Intermedia)" in sim["backtesting_temporal"]
    assert "2024 (Presidencial)" in sim["backtesting_temporal"]
