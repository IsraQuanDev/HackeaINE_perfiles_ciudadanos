from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
PROFILES_PATH = BASE_DIR / "data" / "processed" / "perfiles_municipio.parquet"
META_PATH = BASE_DIR / "data" / "processed" / "clustering_model_metadata.json"
SEG_DOC = BASE_DIR / "docs" / "segmentacion.md"


def test_clustering_artifacts_exist() -> None:
    assert PROFILES_PATH.exists(), "Falta data/processed/perfiles_municipio.parquet"
    assert META_PATH.exists(), "Falta data/processed/clustering_model_metadata.json"
    assert SEG_DOC.exists(), "Falta docs/segmentacion.md"


def test_clustering_constraints_and_quality() -> None:
    df = pd.read_parquet(PROFILES_PATH)
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))

    assert df["cve_geo"].is_unique
    assert df["cluster_id"].notna().all()
    assert (df["probabilidad_pertenencia"] > 0.0).all() and (
        df["probabilidad_pertenencia"] <= 1.0
    ).all()

    k = int(meta["winner_k"])
    assert 4 <= k <= 7, f"El número de perfiles debe estar entre 4 y 7, obtenido: {k}"

    # Verificar tamaño mínimo de cluster >= 3% de municipios
    props = df["cluster_id"].value_counts(normalize=True)
    assert (props >= 0.03).all(), f"Algún cluster tiene menos del 3% de municipios:\n{props}"

    # Verificar que k en [3..10] fue evaluado en la grilla
    k_grid = pd.DataFrame(meta["k_grid_results"])
    km_ks = set(k_grid[k_grid["metodo"] == "A_KMeans_Robust"]["k"].tolist())
    assert km_ks == set(range(3, 11)), f"Faltan valores de k en [3..10]: {km_ks}"
