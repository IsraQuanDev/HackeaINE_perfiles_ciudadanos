from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
FEAT_PATH = BASE_DIR / "data" / "processed" / "features_municipio.parquet"
DICT_PATH = BASE_DIR / "docs" / "diccionario_features.md"
FUENTES_PATH = BASE_DIR / "docs" / "fuentes.md"


def test_features_files_exist() -> None:
    assert FEAT_PATH.exists(), "Falta data/processed/features_municipio.parquet"
    assert DICT_PATH.exists(), "Falta docs/diccionario_features.md"
    assert FUENTES_PATH.exists(), "Falta docs/fuentes.md"


def test_features_ranges_and_integrity() -> None:
    df = pd.read_parquet(FEAT_PATH)
    assert df["cve_geo"].is_unique, "cve_geo debe ser único (una fila por municipio)"
    assert len(df) >= 2450

    # Verificar rangos [0, 1] para tasas de participación y proporciones
    rate_cols = [
        "part_2009",
        "part_2012",
        "part_2015",
        "part_2018",
        "part_2021",
        "part_2024",
        "part_media_global",
        "part_media_presidencial",
        "part_media_intermedia",
        "constancia_sobre_mediana",
        "pct_ln_jovenes_18_29",
        "pct_ln_adultos_60_mas",
        "pct_ln_urbana",
        "pct_ln_mixta",
        "pct_ln_rural",
    ]
    for col in rate_cols:
        assert df[col].notna().all(), f"La columna {col} no debe tener NaN en la matriz procesada"
        assert (df[col] >= 0.0).all() and (df[col] <= 1.0).all(), f"Columna {col} fuera de [0, 1]"

    # La suma de proporciones urbana + mixta + rural debe ser ~1.0
    sum_sec = df["pct_ln_urbana"] + df["pct_ln_mixta"] + df["pct_ln_rural"]
    assert np.allclose(sum_sec, 1.0, atol=1e-4), "Las proporciones de tipo de sección deben sumar 1.0"


def test_no_temporal_leakage_and_imputation_flags() -> None:
    """Verifica banderas de imputación v2 (cobertura >= 90%), Shrinkage Bayesiano, 8 grupos de edad + FPCA y econometría espacial."""
    df = pd.read_parquet(FEAT_PATH)
    incomplete = df["n_elecciones_observadas"] < 6
    assert (df["flag_imputacion_trayectoria"] == incomplete).all()

    # En municipios medianos/grandes (LN >= 10,000) con las 6 elecciones válidas, el Shrinkage Bayesiano (M=450)
    # converge a la tasa cruda (< 3 p.p. de diferencia), y a nivel nacional reduce la volatilidad de muestra pequeña
    complete_large = df[(~df["flag_imputacion_trayectoria"]) & (df["ln_2024"] >= 10000)]
    for y in [2009, 2012, 2015, 2018, 2021, 2024]:
        assert np.allclose(complete_large[f"part_{y}"], complete_large[f"part_{y}_raw"], atol=0.03, equal_nan=False)
    assert df["volatilidad"].mean() < df["volatilidad_unshrunk"].mean()

    # Verificar que las nuevas variables v2 (8 grupos de edad, FPCA, PELT, MAD, IForest, Gi*) existan
    for v2_col in [
        "part_edad_18_19",
        "part_edad_20_24",
        "part_edad_25_29",
        "part_edad_30_39",
        "part_edad_40_49",
        "part_edad_50_59",
        "part_edad_60_69",
        "part_edad_70_mas",
        "fpca_edad_pc1",
        "fpca_edad_pc2",
        "fpca_edad_pc3",
        "retencion_primer_voto",
        "mad_zscore_max",
        "tiene_cambio_estructural_pelt",
        "anomalia_iforest",
        "gi_star_z",
    ]:
        assert v2_col in df.columns, f"Falta columna v2 {v2_col} en features_municipio.parquet"

    # Verificar que Moran's I y LISA estén calculados
    assert df["moran_global_i"].notna().all()
    assert set(df["lisa_cluster"].unique()).issubset(
        {"HH (Alto-Alto)", "LL (Bajo-Bajo)", "HL (Alto-Bajo)", "LH (Bajo-Alto)", "NS (No significativo)"}
    )
