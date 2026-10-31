# Modelo Predictivo 2027, Validación Temporal y Simulador What-If (`docs/forecast.md`)

> **AVISO METODOLÓGICO (NO CAUSAL):** Las proyecciones a la elección intermedia federal de 2027 y el simulador *what-if* constituyen una herramienta de **priorización territorial y planeación operativa**, no un modelo de inferencia causal.

## 1. Diseño de Validación Temporal Estricta (Backtesting Out-of-Time)

- **Entrenamiento sin fugas temporales:** Para cada corte de prueba (`2018`, `2021`, `2024`), las variables explicativas se construyen únicamente con elecciones estrictamente previas ($t < t_{\text{test}}$).
- **Modelo principal:** `LightGBM` con pérdida $L_1$ regularizada sobre el residual respecto al promedio histórico del mismo tipo de elección (`presidencial` vs. `intermedia`), acompañado de **Regresión Cuantílica Conformalizada (CQR)** para los intervalos de predicción al 80% ($[q_{10}, q_{90}]$).
- **Baseline ingenuo de referencia:** Promedio histórico municipal de las elecciones previas del mismo tipo.

## 2. Resultados Globales del Backtesting (2018, 2021, 2024)

| Corte Electoral | Modelo | MAE (p.p. $\downarrow$) | RMSE (p.p. $\downarrow$) | Cobertura Empírica Intervalo 80% | Ancho Medio Intervalo (p.p.) |
| :--- | :--- | ---: | ---: | ---: | ---: |
| **2018 (Presidencial)** | `LightGBM + Conformal` | **8.62 p.p.** | **13.28 p.p.** | `81.5%` | `28.1 p.p.` |
| **2018 (Presidencial)** | `Baseline Ingenuo (Mismo Tipo)` | 7.98 p.p. | 12.53 p.p. | `78.5%` | `25.5 p.p.` |
| **2021 (Intermedia)** | `LightGBM + Conformal` | **12.58 p.p.** | **16.28 p.p.** | `61.3%` | `28.8 p.p.` |
| **2021 (Intermedia)** | `Baseline Ingenuo (Mismo Tipo)` | 13.78 p.p. | 17.73 p.p. | `50.7%` | `25.7 p.p.` |
| **2024 (Presidencial)** | `LightGBM + Conformal` | **7.63 p.p.** | **11.37 p.p.** | `86.2%` | `28.4 p.p.` |
| **2024 (Presidencial)** | `Baseline Ingenuo (Mismo Tipo)` | 8.14 p.p. | 11.80 p.p. | `75.7%` | `25.6 p.p.` |

## 3. Métricas de Backtesting por Perfil (Corte Intermedia 2021 — Análogo a 2027)

| Perfil | MAE LightGBM (p.p.) | RMSE LightGBM (p.p.) | Cobertura 80% LightGBM | MAE Baseline Ingenuo (p.p.) |
| :---: | ---: | ---: | ---: | ---: |
| `Perfil_0` | **7.81 p.p.** | 10.49 p.p. | `77.2%` | 8.64 p.p. |
| `Perfil_1` | **13.23 p.p.** | 15.86 p.p. | `48.7%` | 15.04 p.p. |
| `Perfil_2` | **24.05 p.p.** | 26.61 p.p. | `29.3%` | 27.04 p.p. |
| `Perfil_3` | **17.48 p.p.** | 21.68 p.p. | `77.2%` | 17.52 p.p. |
| `Perfil_4` | **8.55 p.p.** | 10.86 p.p. | `74.3%` | 8.33 p.p. |
| `Perfil_5` | **10.78 p.p.** | 13.44 p.p. | `65.0%` | 12.11 p.p. |

## 4. Honestidad Metodológica: ¿Dónde Falla el Modelo?

El análisis de residuales out-of-time demuestra que el modelo presenta errores elevados (>15 puntos porcentuales) en tres situaciones específicas que el usuario debe considerar:
1. **Municipios con Lista Nominal pequeña (`flag_baja_confiabilidad = true`, LN < 1,000):** Donde la concurrencia o suspensión en un par de secciones rurales desplaza drásticamente el porcentaje municipal.
2. **Concurrencia asimétrica con elecciones locales de gubernatura o alcaldía altamente competitivas:** El CCPC mide participación en casillas federales, pero la tracción de elecciones locales concurrentes introduce choques idiosincráticos de un solo ciclo.
3. **Conflictos sociales/comunitarios o incidentes de no instalación de casillas:** Que reducen abruptamente `SV` en un año particular y se revierten en el siguiente.

### Ejemplos Reales de Mayor Error en Backtesting 2024

| `cve_geo` | Municipio | Entidad | Perfil | Participación Real | Predicción | Error Absoluto (p.p.) | Baja Confiabilidad |
| :---: | :--- | :--- | :---: | ---: | ---: | ---: | :---: |
| `26031` | Oquitoa | SONORA | Perfil 3 | 0.0% | 81.7% | `81.7 p.p.` | `True` |
| `26006` | Atil | SONORA | Perfil 3 | 0.0% | 80.5% | `80.5 p.p.` | `True` |
| `26016` | Cucurpe | SONORA | Perfil 3 | 0.0% | 77.8% | `77.8 p.p.` | `True` |
| `26043` | Tubutama | SONORA | Perfil 3 | 0.0% | 72.2% | `72.2 p.p.` | `False` |
| `07066` | PantelhÃ³ | CHIAPAS | Perfil 3 | 0.0% | 68.5% | `68.5 p.p.` | `False` |

## 5. Proyección 2027 (Elección Intermedia) y Simulador What-If por Perfil

- **Lista Nominal Nacional Proyectada 2027:** `103,094,135` electores.
- **Votantes Esperados Escenario Base 2027:** `49,866,421` (`48.37%`).
- **Municipios identificados como Zonas en Riesgo de Abstención:** `420` municipios.

| Perfil | Municipios | Zonas en Riesgo | LN Proyectada 2027 | Part. Proyectada 2027 | Votantes Adicionales por `+1 p.p.` | Votantes Adicionales por `+3 p.p.` | Votantes Adicionales por `+5 p.p.` |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Perfil 0** | 539 | 142 | 8,481,311 | `61.24%` | `+84,813` | `+254,439` | `+424,066` |
| **Perfil 1** | 378 | 61 | 7,255,975 | `55.98%` | `+72,560` | `+217,679` | `+362,799` |
| **Perfil 2** | 440 | 6 | 13,783,316 | `52.43%` | `+137,833` | `+413,499` | `+689,166` |
| **Perfil 3** | 79 | 10 | 747,225 | `51.82%` | `+7,472` | `+22,417` | `+37,361` |
| **Perfil 4** | 553 | 178 | 61,061,638 | `45.26%` | `+610,616` | `+1,831,849` | `+3,053,082` |
| **Perfil 5** | 488 | 23 | 11,764,670 | `45.59%` | `+117,647` | `+352,940` | `+588,234` |
