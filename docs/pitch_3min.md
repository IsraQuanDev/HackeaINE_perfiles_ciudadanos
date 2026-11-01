# Guión de Pitch de 3 Minutos (Plan v2 · Hackatón INE Reto 1)

## Gancho inicial (0:00 – 0:30) — *Datos correctos antes que gráficas bonitas*
- **"Un dashboard hermoso con cifras equivocadas pierde ante uno riguroso con cifras verificables. Nosotros construimos ambos."**
- Al auditar los 8 conjuntos de datos de la Plataforma de Conteos Censales de Participación Ciudadana (CCPC 2009–2024, más de **407,000 registros seccionales y municipales** y **98.33 millones de personas en Lista Nominal**), descubrimos un hallazgo crítico: en 76 celdas municipio-año (como **Atil, Cucurpe, Oquitoa, Tubutama e Higueras en 2024**, o **Rayones y Magdalena Ocotlán en 2009**), el 100% de la Lista Nominal aparecía en el campo `NS` (*cuadernillos no disponibles o reservados*).
- Tratar esos faltantes como `0.0%` de participación inflaba artificialmente la volatilidad de esos municipios de **4.8 p.p. a 29.7 p.p.** y distorsionaba el clustering, el diagrama Sankey y el backtesting. Nuestra primera entrega al INE es esa **auditoría de calidad con regla estricta de cobertura `(SV + NV)/LN >= 90%`** y normalización **UTF-8 NFC** libre de mojibake.

## Qué revelan los datos y cómo segmentamos (0:30 – 1:30) — *Curva de 8 edades, Econometría Espacial y Consenso*
- Explotamos los **8 grupos etarios completos del CCPC** (`18–19` hasta `70+` años) mediante Análisis de Componentes Principales Funcional (**FPCA**) y seguimiento de cohortes de primer voto: demostramos empíricamente que las juventudes de `18–19` años sí acuden a su primer voto (`55.6%` en 2024), pero la participación sufre un **"valle post-primer voto"** entre los `20 y 29` años (`-9.7 p.p.`) antes de recuperarse hasta `72.7%` en `60–69` años.
- Aplicamos **Empirical Bayes Beta-Binomial Shrinkage** para estabilizar municipios pequeños y **Econometría Espacial** ($I\text{ de Moran} = 0.4526, p = 0.001$, LISA y Getis-Ord $G_i^*$).
- Nuestro **Ensemble de Consenso Ponderado por Lista Nominal (`k=6`, estabilidad bootstrap `ARI = 0.905`)** identifica 6 perfiles territoriales claros, cada uno anclado en su **municipio prototipo medoide real** (etiquetado explícitamente como `[DATO REAL]`) y con estrategias diferenciadas alineadas a la **ENCCÍVICA y DECEyEC**.
- **Honestidad metodológica (Principio #5):** Entrenamos y evaluamos un **Autoencoder Profundo (Deep Learning)**; al no superar de forma sustantiva al ensamble clásico (`Silhouette 0.1455 vs 0.1422`) y restar interpretabilidad, lo reportamos transparentemente y mantuvimos el modelo auditable.

## Prospectiva 2027, Simulador Knapsack y Guardrails Éticos (1:30 – 2:30)
- Para proyectar la elección intermedia de **2027**, diseñamos un **Modelo Jerárquico en Dos Etapas** (Etapa 1: régimen macro de intermedia en escenarios *Bajo, Base y Alto*; Etapa 2: desviación municipal persistente con *partial pooling* + LightGBM) calibrado con **Mondrian Conformalized Quantile Regression (CQR)** por perfil.
- En el backtesting de la intermedia 2021, redujimos el error (MAE) de `12.58 p.p.` a **`9.81 p.p.`**, superando a los 3 baselines de referencia y logrando una **cobertura empírica exacta del `80.0%`** en los intervalos nominales al 80%.
- El **Simulador What-If (explícitamente etiquetado como asociativo, no causal)** integra propagación Monte Carlo, un **Optimizador Presupuestal Knapsack** para asignar brigadas DECEyEC donde generan mayor retorno cívico, y el protocolo de **evaluación experimental A/B por clusters**.
- Finalmente, el agente **"Pregúntale a los Datos" (Text-to-SQL sobre DuckDB)** responde en milisegundos con SQL verificable y **rechaza activamente** preguntas sobre partidos políticos o reidentificación individual.

## Cierre (2:30 – 3:00)
- Todo corre de forma 100% reproducible (`make all`, semilla `42`), con mapas poligonales reales a tres escalas (2,477 municipios, 251 distritos y 32 estados), exportación de Ficha Municipal en PDF y suite completa de pruebas automatizadas.
