.PHONY: all ingest features cluster explain forecast dl llm export test lint clean

PYTHON ?= python -u

all: ingest features cluster explain dl forecast llm export test lint

ingest:
	$(PYTHON) -m src.ingest.pipeline

features:
	$(PYTHON) -m src.features.pipeline

cluster:
	$(PYTHON) -m src.clustering.pipeline

explain:
	$(PYTHON) -m src.explain.pipeline

forecast:
	$(PYTHON) -m src.forecast.pipeline

dl:
	$(PYTHON) -m src.clustering.deep_autoencoder

llm:
	$(PYTHON) -m src.llm.pipeline

export:
	$(PYTHON) -m src.api.export_dashboard_bundle

test:
	$(PYTHON) -m pytest tests/

lint:
	$(PYTHON) -m ruff check src/ tests/

clean:
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in [pathlib.Path('data/interim'), pathlib.Path('data/processed')]]; [p.unlink(missing_ok=True) for p in [pathlib.Path('data/ccpc.duckdb')]]"
