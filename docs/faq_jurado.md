# Las 10 Preguntas Más Difíciles del Jurado y Respuestas Técnicas (`docs/faq_jurado.md`)

### 1. ¿Cómo garantizan que sus perfiles no incurren en la falacia ecológica al proponer estrategias de comunicación ciudadana?
**Respuesta:** La unidad de observación, modelado y evaluación es estrictamente el **territorio municipal (`cve_geo`)**, nunca el individuo. En la interfaz, en el `README.md` y en los prompts de la capa LLM incluimos candados explícitos que prohíben atribuir rasgos psicológicos o motivaciones personales a los habitantes. Las estrategias propuestas (p. ej., brigadas itinerantes en zonas con >60% de secciones rurales o foros universitarios en municipios con alta brecha entre 60+ y 18–29 años) son **intervenciones de política pública focalizadas en el entorno territorial e institucional**, no micro-segmentación individual.

### 2. ¿Por qué eligieron K-Means con `RobustScaler` sobre métodos más sofisticados como HDBSCAN, DTW o el Autoencoder Temporal en PyTorch?
**Respuesta:** Aplicamos el Principio Inquebrantable #5 (**Honestidad Metodológica**). Evaluamos los cinco enfoques clásicos y el Autoencoder Temporal (`dim=6`) bajo las mismas métricas cuantitativas: Silhouette en el espacio original de variables, Davies-Bouldin, Calinski-Harabasz, tamaño mínimo de cluster ($\ge 3\%$) y estabilidad Bootstrap ($n=100$, Adjusted Rand Index).
- **HDBSCAN** es excelente para aislar casos atípicos (`es_atipico_hdbscan`), pero deja sin perfil asignado a un porcentaje de municipios que el INE necesita atender operativamente.
- **DTW (`TimeSeriesKMeans`)** agrupa bien el nivel medio de la serie pero ignora la brecha de género, la brecha generacional y la ruralidad.
- **El Autoencoder Temporal** logra baja pérdida de reconstrucción, pero no supera al modelo `A_KMeans_Robust` en separación dentro del espacio observable y reduce la trazabilidad directa de cada variable ante tomadores de decisiones. Por ello conservamos `A_KMeans_Robust` como modelo ganador y usamos HDBSCAN como detector complementario de municipios atípicos.

### 3. ¿Cómo evitaron que la segmentación fuera trivialmente "alta, media y baja participación"?
**Respuesta:** Diseñamos explícitamente la matriz de segmentación con **10 variables donde 9 miden dinámica, estructura y brechas**: caída presidencial $\rightarrow$ intermedia (`caida_presidencial_intermedia`), pendiente temporal robusta Theil-Sen (`pendiente_tendencia`), volatilidad inter-elección (`volatilidad`), constancia sobre la mediana anual (`constancia_sobre_mediana`), nivel y tendencia de la brecha de género (`brecha_genero_media`, `brecha_genero_tendencia`), brecha generacional (`brecha_generacional_60_vs_18_29`), ruralidad electoral (`pct_ln_rural`) y crecimiento demográfico del padrón (`cagr_ln_2009_2024`). El análisis SHAP demuestra que los perfiles se separan por la magnitud de la caída en elecciones intermedias, la dirección de su pendiente temporal y su composición urbano-rural.

### 4. Entre 2009 y 2024 se crearon nuevos municipios en México y hubo redistritaciones (DERFE 2021 vs. 2023). ¿Cómo manejaron ese problema sin perder ni duplicar votos?
**Respuesta:** Construimos la tabla puente [`puente_municipio_anio.parquet`](file:///c:/Users/52477/Desktop/hackaton2INE/data/processed/puente_municipio_anio.parquet) que audita los 2,477 municipios registrados entre 2009 y 2024:
- Identifica con precisión los municipios con panel completo (6 elecciones) frente a los municipios de nueva creación (como Bacalar y Puerto Morelos en Quintana Roo, San Quintín y San Felipe en Baja California, o Seybaplaya y Dzitbalché en Campeche).
- Preservamos las tasas observadas sin alterar en `part_YYYY_raw`, y para algoritmos que requieren vectores completos de longitud 6 imputamos únicamente los años previos a la creación del municipio con la mediana estatal de ese año, activando la bandera `flag_imputacion_trayectoria = true`.
- Además, nuestro test automatizado `test_entity_voter_sums_match_source_exactly` verifica que la suma de votantes y lista nominal por entidad y año coincida al 100% con los 194 archivos CSV fuente.

### 5. ¿Cómo incorporaron los archivos de Voto Anticipado 2024 y Prisión Preventiva 2024 si tienen esquemas distintos a los conteos ordinarios?
**Respuesta:** Inspeccionamos sus diccionarios y registros antes de diseñar el esquema unificado:
- **Voto Anticipado 2024** trae clave municipal (`MPIOCVE`), distrito (`DEF`, `DEL`) y `SEXO`, pero no `EDAD` ni `LN`. Se integró al esquema largo bajo `modalidad = 'anticipado'` y a nivel municipal calculamos la tasa `tasa_voto_anticipado_por_10k` (votantes anticipados por cada 10,000 inscritos en Lista Nominal 2024).
- **Prisión Preventiva 2024** solo trae entidad (`ESTADO`), distrito federal (`DEF`) y `SEXO`, **sin municipio**. Cumpliendo la prohibición estricta de inventar datos, no lo repartimos artificialmente entre municipios: se almacena con `cve_mun = '000'` y `modalidad = 'prision_preventiva'`, integrándose de manera exacta en las vistas por Distrito Federal (`v_distrito_eleccion`) y Entidad (`v_entidad_eleccion`).

### 6. Con apenas 6 cortes temporales federales (2009, 2012, 2015, 2018, 2021, 2024), ¿cómo justifican un modelo predictivo hacia 2027 sin caer en sobreajuste o fuga de datos?
**Respuesta:** Tres decisiones técnicas previenen el sobreajuste y las fugas:
1. **Estructura de panel transversal-temporal ($N \times T$):** Aunque hay 6 cortes temporales, cada corte tiene ~2,477 municipios, lo que brinda miles de transiciones municipio-elección.
2. **Modelado sobre el residual del ciclo análogo:** En lugar de extrapolar series cortas en el vacío, el modelo `LightGBM` predice el ajuste regularizado ($L_1$, árboles de profundidad máxima 4) sobre el promedio histórico de elecciones del **mismo tipo** (`intermedia` vs. `presidencial`), usando únicamente rezagos anteriores ($t - 3, t - 6$).
3. **Backtesting honesto out-of-time (2018, 2021, 2024):** Documentamos en `docs/forecast.md` tanto la mejora en MAE/RMSE frente al baseline ingenuo como los casos donde el modelo falla (municipios con `LN < 1,000` o choques políticos locales concurrentes).

### 7. ¿Cómo se calculan los intervalos de predicción al 80% para 2027 y por qué son confiables?
**Respuesta:** Combinamos **Regresión Cuantílica en LightGBM** ($\alpha = 0.10$ y $\alpha = 0.90$) con **Calibración Conformal Temporal (Conformalized Quantile Regression - CQR)** ponderada por la volatilidad histórica municipal. Esto garantiza que la cobertura empírica out-of-time del intervalo al 80% se mantenga calibrada alrededor del 80% real, ensanchando el intervalo en municipios históricamente volátiles y estrechándolo en municipios estables.

### 8. El Simulador What-If muestra cuántos votantes adicionales habría si un perfil sube $N$ puntos. ¿No induce eso a pensar que la estrategia causará ese aumento?
**Respuesta:** Por diseño, tanto el JSON de salida (`simulador_what_if.json`) como el banner superior del componente en el dashboard muestran una advertencia destacada: **"Ejercicio aritmético de priorización territorial, NO causal"**. Su función para el INE es responder una pregunta de asignación presupuestal y logística: *¿en qué perfiles un incremento de 1 a 3 puntos porcentuales representa el mayor volumen absoluto de ciudadanía participando dada su Lista Nominal proyectada a 2027?* Para medir causalidad real, proponemos el protocolo de pruebas A/B por conglomerados en los siguientes pasos.

### 9. ¿Cómo evitan que el LLM alucine cifras en las narrativas o ejecute SQL destructivo en el chat?
**Respuesta:** Implementamos tres barreras deterministas en código (`src/llm/`):
1. **Verificador automático de cifras (`verify_narrative_grounding`):** Extrae recursivamente todos los valores numéricos del JSON de entrada de ese perfil y comprueba que cada número citado en `datos_clave[*].evidencia` exista con exactitud matemática en el JSON fuente; si se introduce cualquier número ajeno, lanza `ValueError` (verificado en `tests/eval_chat.py`).
2. **Guardrails SQL (`validate_safe_sql`):** Bloquea cualquier sentencia que no inicie con `SELECT`/`WITH`, rechaza palabras reservadas DDL/DML (`DROP, DELETE, UPDATE, INSERT, COPY, PRAGMA`), valida cada tabla en `FROM`/`JOIN` contra la lista blanca de `docs/capa_semantica.yaml` e inyecta `LIMIT <= 100`.
3. **Detección de preguntas no respondibles:** Preguntas sobre partidos políticos, ganadores de elecciones o datos individuales se rechazan antes de tocar la base de datos.

### 10. ¿Qué pasa con las celdas pequeñas donde podría identificarse si un grupo reducido de personas votó?
**Respuesta:** Cumplimos el Principio Inquebrantable #1 en dos niveles:
1. Eliminamos la granularidad individual de edad año por año (`18..125`) agrupando en tres grandes bandas etarias (`18-29`, `30-59`, `60+`) y agregando a nivel municipal, distrital y estatal.
2. En el esquema unificado marcamos `celda_pequena_lt10 = true` para cualquier celda con `lista_nominal < 10` (o `votantes < 10`), y en las vistas analíticas de DuckDB (`v_municipio_eleccion`, `v_distrito_eleccion`) toda tasa cuyo denominador sea menor a 10 se suprime devolviendo `NULL`.
