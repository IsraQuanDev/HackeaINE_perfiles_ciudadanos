from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DL_JSON = BASE_DIR / "data" / "processed" / "deep_learning_eval.json"
DL_DOC = BASE_DIR / "docs" / "deep_learning.md"


def test_deep_learning_evaluation_exists_and_valid() -> None:
    assert DL_JSON.exists(), "Falta data/processed/deep_learning_eval.json"
    assert DL_DOC.exists(), "Falta docs/deep_learning.md"
    data = json.loads(DL_JSON.read_text(encoding="utf-8"))
    assert 4 <= data["latent_dim"] <= 8
    assert "conclusion_explicita" in data
    assert "baseline_metrics" in data and "autoencoder_metrics" in data
