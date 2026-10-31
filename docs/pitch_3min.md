# Guion de Pitch (3 Minutos) y Plan B de Demo Offline (`docs/pitch_3min.md`)

## 1. Guion Estructurado de 3 Minutos (180 segundos)

### [0:00 - 0:25] El Problema: Las campañas uniformes frente a un país electoralmente heterogéneo
> "En México, la diferencia entre los municipios con mayor y menor participación electoral supera los **50 puntos porcentuales**, y en cientos de municipios la asistencia a las urnas cae más de **20 puntos** cuando pasamos de una elección presidencial a una intermedia como la que viviremos en **2027**. Sin embargo, muchas estrategias de promoción del voto siguen tratando al territorio como si fuera homogéneo o clasificándolo simplemente en 'alta, media y baja participación'."

### [0:25 - 0:55] El Hallazgo Sorprendente en los Conteos Censales 2009–2024
> "Al procesar de forma íntegra las **54.8 millones de filas** de los Conteos Censales de Participación Ciudadana del INE entre **2009 y 2024** (incluyendo Voto Anticipado y Prisión Preventiva 2024), descubrimos un patrón estructural determinante:
> 1. La participación territorial tiene una **fuerte autocorrelación espacial positiva** ($I \text{ de Moran} = 0.478, p = 0.002$).
> 2. En las secciones rurales la participación media supera a muchas zonas urbanas, pero en los centros urbanos la **brecha generacional entre adultos mayores (60+) y jóvenes (18–29)** rebasa los **18 puntos porcentuales**, y la caída en elecciones intermedias explica la mayor pérdida neta de votantes."

### [0:55 - 1:30] Los Perfiles Territoriales con Nombre y Explicabilidad SHAP
> "Evaluamos cinco familias de algoritmos (K-Means con `RobustScaler`, Modelos de Mezclas Gaussianas por BIC, HDBSCAN, series de tiempo con Dynamic Time Warping y clustering espacial) y un Autoencoder Temporal profundo. Seleccionamos el modelo ganador por estabilidad bootstrap ($n=100$) e interpretabilidad SHAP, identificando perfiles accionables como:
> - **Cohesión Comunitaria Sostenida:** Municipios con participación constante tanto en presidenciales como en intermedias.
> - **Participación Rural Constante:** Territorios con liderazgo cívico femenino positivo (`Mujeres > Hombres`).
> - **Impulso Cívico en Ascenso:** Municipios con pendiente positiva sostenida 2009–2024.
> - **Movilización Presidencial Selectiva:** Municipios que acuden masivamente en presidenciales pero se desploman en intermedias.
> - **Dinámica Urbana Intermitente** y **Prioridad de Reactivación Cívica**."

### [1:30 - 2:10] Demo en Vivo: De la Transición de Perfiles al Simulador 2027 y Chat SQL
> *(En pantalla: Mapa Coroplético $\rightarrow$ Diagrama Sankey $\rightarrow$ Buscador Municipal $\rightarrow$ Simulador What-If $\rightarrow$ Chat SQL)*
> "En el diagrama **Sankey de ventanas móviles** (`2009-2015` a `2018-2024`), observamos cómo más del 30% de los municipios transitaron de perfil. En el buscador municipal podemos inspeccionar cualquier municipio que transitó hacia *Impulso Cívico en Ascenso*, compararlo contra sus vecinos espaciales y contra la media nacional.
> En el panel **Proyección 2027**, nuestro modelo `LightGBM` con **Regresión Cuantílica Conformalizada** (validado sin fugas temporales en 2018, 2021 y 2024) proyecta la participación intermedia con intervalos al 80% e identifica las **zonas en riesgo prioritario**. Y con el agente **'Pregúntale a los datos'**, cualquier vocalía puede consultar en lenguaje natural el catálogo `DuckDB` recibiendo la tabla y el SQL exacto, o un rechazo ético inmediato si pregunta por partidos o datos personales."

### [2:10 - 2:40] Estrategias Diferenciadas con KPIs Verificables y Rigor Ético
> "Cada perfil se conecta con una estrategia fundamentada en la **ENCCÍVICA** y los programas de la **DECEyEC**, con **línea base real verificada automáticamente** contra el JSON estadístico: desde circuitos universitarios *'Mi Primer Voto 2027'* donde domina la brecha juvenil, hasta Diálogos Comunitarios donde domina la caída intermedia. Todo bajo tres candados éticos: **cero datos individuales**, **supresión de celdas `< 10`**, y advertencia explícita contra la **falacia ecológica** y el uso **no causal** del simulador."

### [2:40 - 3:00] Siguientes Pasos: Evaluación de Impacto mediante Pruebas A/B Territoriales
> "Para pasar de la priorización a la evidencia causal en 2027, proponemos un diseño experimental de **Pruebas A/B aleatorizadas por conglomerados (secciones/municipios pareados dentro de cada perfil)** junto con DECEyEC, midiendo el levantamiento neto en los cuadernillos censales 2027."

---

## 2. Plan B de Demo (Modo 100% Offline y Guion para Video de Respaldo)

### Modo Offline Integrado
1. **Cero dependencia de internet o APIs externas en tiempo de demo:**
   - Todos los artefactos (`features_municipio.parquet`, `perfiles_municipio.parquet`, `perfiles_caracterizacion.json`, `transiciones.json`, `proyeccion_2027.parquet`, `simulador_what_if.json`, `llm_perfiles_narrativas_estrategias.json`) están precalculados y servidos localmente en `/app/public/data/`.
   - El motor de consultas del dashboard y el agente Text-to-SQL operan **100% en local** sin requerir llaves de API externas ni conexión de red.
2. **Secuencia de Video de Respaldo (90 segundos sin cortes):**
   - **Toma 1 (0:00–0:20):** Vista del Mapa Coroplético Nacional filtrando por perfil y mostrando tooltip municipal con trayectoria 2009–2024.
   - **Toma 2 (0:20–0:40):** Selección de las Tarjetas de Perfil (radar multivariable, narrativa verificada con evidencias resaltadas y estrategia ENCCÍVICA con KPI).
   - **Toma 3 (0:40–0:55):** Diagrama Sankey de transiciones entre ventanas temporales y buscador "¿Qué perfil tiene mi municipio?" comparando contra entidad y país.
   - **Toma 4 (0:55–1:15):** Panel de Proyección 2027 (intervalos al 80% + tabla de zonas en riesgo) y movimiento del deslizador del Simulador What-If mostrando el aviso de "No Causal".
   - **Toma 5 (1:15–1:30):** Ejecución en vivo de 2 preguntas en "Pregúntale a los datos" (una consulta analítica con SQL visible y una pregunta sobre partidos políticos mostrando el rechazo ético automático) y cierre en la pestaña "Metodología y Límites".
