---
name: run-pipeline
description: Ejecuta de principio a fin el pipeline reproducible de ingesta, ingeniería de variables, segmentación territorial, explicabilidad SHAP, evaluación Deep Learning, proyección 2027, capa LLM, exportación de bundle del dashboard y suite completa de pruebas (pytest + ruff).
---

# Workflow `/run-pipeline`: Regeneración Completa del Proyecto CCPC INE (2009–2024)

## Cuándo usar este skill
Usa este skill cuando necesites regenerar desde cero o actualizar los perfiles territoriales de participación, reentrenar el modelo predictivo hacia 2027, regenerar las narrativas y estrategias verificadas de la capa LLM o validar la integridad completa del repositorio (`make all`).

## Pasos de Ejecución
1. **Fase 1 (Ingesta y Catálogo DuckDB):**
   ```powershell
   python -u -m src.ingest.pipeline
   ```
2. **Fase 2 (Ingeniería de Variables, Enriquecimiento y Moran/LISA):**
   ```powershell
   python -u -m src.features.pipeline
   ```
3. **Fase 3 (Segmentación Territorial Multivariable y Validación Bootstrap):**
   ```powershell
   python -u -m src.clustering.pipeline
   ```
4. **Fase 4 (Explicabilidad SHAP y Dinámica de Ventanas Móviles / Sankey):**
   ```powershell
   python -u -m src.explain.pipeline
   ```
5. **Fase 6 (Evaluación Condicional de Autoencoder Temporal vs. Baseline):**
   ```powershell
   python -u -m src.clustering.deep_autoencoder
   ```
6. **Fase 5 (Proyección 2027 con LightGBM Cuantílico Conformal y Simulador What-If):**
   ```powershell
   python -u -m src.forecast.pipeline
   ```
7. **Fase 7 (Capa LLM: Narrativas con Verificador de Cifras, Estrategias y Chat SQL):**
   ```powershell
   python -u -m src.llm.pipeline
   ```
8. **Exportación al Dashboard (`/app/public/data`) y Validación QA (`pytest` + `ruff`):**
   ```powershell
   python -u -m src.api.export_dashboard_bundle
   python -u -m pytest tests/
   python -u -m ruff check src/ tests/
   ```
