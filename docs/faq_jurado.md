# Preguntas Frecuentes del Jurado (FAQ Técnico y Metodológico · Plan v2)

## 1. ¿Por qué en su diagnóstico inicial había municipios con 0% de participación y cómo lo resolvieron?
- **Causa raíz demostrada con SQL:** En los archivos crudos del CCPC 2009–2024 existen tres campos de conteo: `SV` (*Sí Votó*), `NV` (*No Votó*) y `NS` (*No Especificado / cuadernillo no disponible o reservado*). En **76 celdas municipio-año** (incluyendo **Atil, Cucurpe, Oquitoa, Tubutama e Higueras en 2024**, y **Rayones y Magdalena Ocotlán en 2009**), `SV = 0`, `NV = 0` y `NS = Lista Nominal` (cobertura de captura del `0%`). Además, en 3 municipios de Oaxaca en 2012 (`20253, 20273, 20327`), `SV = 0` y `NV = LN`.
- **Solución en Plan v2:** Definimos explícitamente $\text{cobertura} = \frac{SV + NV}{LN}$ y $\text{participación} = \frac{SV}{SV + NV}$. Toda celda con $\text{cobertura} < 0.90$ o $SV = 0$ se clasifica como **`NA` (sin captura suficiente)** y nunca como `0.0%`. Esto redujo la volatilidad artificial de esos 7 municipios de **29.7 p.p. a 4.8 p.p.** y eliminó por completo los falsos saltos de ±70 p.p. en la tabla de transiciones.

## 2. ¿Cómo aprovecharon la desagregación completa por edad de los diccionarios CCPC?
- En lugar de colapsar prematuramente la edad en 3 grupos, la vista `v_municipio_edad_8grupos` conserva los **8 grupos etarios oficiales** (`18–19`, `20–24`, `25–29`, `30–39`, `40–49`, `50–59`, `60–69`, `70+`) y las **cohortes de primer voto** (`18–20` y `21–23`).
- Aplicamos **Análisis de Componentes Principales Funcional (FPCA)** sobre la curva de 8 edades de cada municipio: el **Componente 1** captura el nivel general de participación a lo largo de la vida, el **Componente 2** mide la pendiente de maduración cívica (diferencia entre adultos mayores y jóvenes), y el **Componente 3** cuantifica la profundidad del **"valle post-primer voto"** entre los `20 y 29` años (`-9.7 p.p.` respecto a `18–19` años en 2024).

## 3. ¿Cómo evitan que municipios muy pequeños dominen o distorsionen la segmentación?
- Combinamos dos mecanismos estadísticos:
  1. **Empirical Bayes Beta-Binomial Shrinkage ($M = 450$):** Contrae suavemente la tasa de municipios con Lista Nominal muy pequeña hacia la media de su entidad federativa en cada elección, reduciendo la desviación estándar del cuartil inferior de LN de `0.0894` a `0.0810`.
  2. **Ensemble de Consenso Ponderado por Lista Nominal (`F_Ensemble_Consenso_LN`):** Combina 5 algoritmos base (K-Means ponderado por LN, GMM con BIC, Ward, Espectral y DTW sobre trayectorias) mediante una matriz de co-asociación, logrando una estabilidad por bootstrap de **`ARI = 0.905`**.

## 4. ¿Por qué el intervalo de predicción al 80% para 2027 ahora sí cubre exactamente el 80%?
- En v1 los intervalos se estimaban con cuantiles sin calibración por régimen ni grupo, logrando solo `61.3%` de cobertura en 2021.
- En v2 implementamos un **Modelo Jerárquico en Dos Etapas** (Etapa 1: nivel macro de elección intermedia; Etapa 2: desviación municipal persistente $z_{i,t} = p_{i,t} - \bar{p}_{nac,t}$ con *partial pooling* + LightGBM) y calibramos los intervalos mediante **Mondrian Conformalized Quantile Regression (CQR)** condicionado por perfil territorial.
- Resultado en backtesting 2021: el MAE bajó de `12.58 p.p.` a **`9.81 p.p.`** (superando a los 3 baselines) y la cobertura empírica alcanzó **`80.0%` global** (`79.9%–80.2%` en cada uno de los 6 perfiles).

## 5. ¿Cómo previenen la falacia ecológica, la atribución causal indebida y las alucinaciones del LLM?
- **Falacia ecológica:** Aviso permanente en el encabezado del dashboard y en cada estrategia: los perfiles describen municipios y secciones agregadas, nunca individuos.
- **No causalidad en el Simulador:** El simulador incluye una advertencia permanente de que las elasticidades son asociativas, reporta intervalos Monte Carlo al 80% y acompaña un protocolo de **Diseño Experimental A/B por clusters** para medir impacto causal real en campo.
- **Cero alucinaciones (`verify_narrative_grounding`):** Ningún texto se genera libremente sin verificación; cada cifra citada en las narrativas y en las tarjetas *"Detectamos que..."* se valida programáticamente contra el JSON de caracterización y consultas SQL sobre `data/ccpc.duckdb`. Además, el ejemplo ilustrativo de cada perfil utiliza el **municipio prototipo medoide real** etiquetado como `[DATO REAL]`.
