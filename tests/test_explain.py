from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CHAR_PATH = BASE_DIR / "data" / "processed" / "perfiles_caracterizacion.json"
TRANS_PATH = BASE_DIR / "data" / "processed" / "transiciones.json"
EXP_DOC = BASE_DIR / "docs" / "explicabilidad.md"


def test_explain_artifacts_exist() -> None:
    assert CHAR_PATH.exists(), "Falta data/processed/perfiles_caracterizacion.json"
    assert TRANS_PATH.exists(), "Falta data/processed/transiciones.json"
    assert EXP_DOC.exists(), "Falta docs/explicabilidad.md"


def test_characterization_and_transitions_schema() -> None:
    char_data = json.loads(CHAR_PATH.read_text(encoding="utf-8"))
    trans_data = json.loads(TRANS_PATH.read_text(encoding="utf-8"))

    assert "perfiles" in char_data and len(char_data["perfiles"]) >= 4
    total_muns = sum(p["n_municipios"] for p in char_data["perfiles"])
    assert total_muns == char_data["referencia_nacional"]["n_municipios_nacional"]

    for p in char_data["perfiles"]:
        assert len(p["top_5_variables_definitorias_shap"]) == 5
        assert len(p["municipios_mas_representativos"]) > 0
        assert len(p["entidades_predominantes"]) > 0

    assert "sankey" in trans_data
    assert len(trans_data["sankey"]["nodes"]) > 0
    assert len(trans_data["sankey"]["links"]) > 0
    assert len(trans_data["top_municipios_cambio"]) > 0
