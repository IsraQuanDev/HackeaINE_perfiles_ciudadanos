# PROYECTO: Perfiles ciudadanos de participación electoral (Hackatón INE, Reto 1)

## Objetivo
Segmentar territorios (municipio como unidad principal; distrito y entidad como vistas agregadas) según su comportamiento de participación 2009-2024 usando la Plataforma de Conteos Censales de Participación Ciudadana (CCPC) del INE, caracterizarlos, nombrarlos narrativamente y proponer estrategias diferenciadas de fomento a la participación.
Entregable final: dashboard interactivo + repo reproducible.

## Principios inquebrantables
1. **SOLO datos agregados y públicos.** Nunca intentes reidentificar personas. Celdas con conteos < 10 se agregan o suprimen (documenta la regla).
2. **Los perfiles describen TERRITORIOS, no individuos (falacia ecológica).** Dilo en la UI y en el README.
3. **Toda cifra mostrada debe ser trazable a un archivo/consulta.** Prohibido inventar datos. Si un dato no está disponible, dilo y usa un enriquecimiento externo documentado.
4. **Reproducibilidad:** seeds fijas, pipeline ejecutable con un solo comando (`make all`), dependencias fijadas.
5. **Honestidad metodológica:** si una técnica compleja (deep learning, etc.) no mejora al baseline, repórtalo así.
6. **Lenguaje no estigmatizante:** nunca etiquetes grupos de forma despectiva.

## Stack
- Python 3.11+, DuckDB + Parquet, Polars, scikit-learn, tslearn, hdbscan, umap-learn, shap, lightgbm, geopandas, esda/libpysal (Moran/LISA), PyTorch (solo autoencoder).
- LLM: API configurable por variable de entorno (sin keys en el repo), salida JSON estructurada.
- Frontend: Next.js + TypeScript + Tailwind, MapLibre GL, ECharts, DuckDB-WASM.
- Calidad: ruff, pytest, pre-commit, tipado con type hints.

## Estructura del repo
- `/data/raw`
- `/data/interim`
- `/data/processed`
- `/notebooks`
- `/src/{ingest,features,clustering,explain,forecast,llm,api}`
- `/app` (frontend)
- `/tests`
- `/docs`
- `Makefile`
- `README.md`

## Forma de trabajar
- Antes de codificar: genera un PLAN y una LISTA DE TAREAS como artefactos y espera aprobación del usuario.
- Al terminar: entrega un REPORTE DE VALIDACIÓN con las pruebas ejecutadas y resultados.
- Commits pequeños con mensajes convencionales (`feat:`, `fix:`, `docs:`).
- Si falta información o hay ambigüedad en los datos, pregunta antes de asumir.
