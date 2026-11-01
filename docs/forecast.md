# Pronóstico 2027 v2 en Dos Etapas, Calibración Mondrian CQR y Optimizador (`docs/forecast.md`)

> **AVISO METODOLÓGICO (NO CAUSAL):** Las proyecciones a la elección intermedia federal de 2027 y el simulador constituyen una herramienta de **priorización territorial**, no un modelo causal.

## 1. Diseño en Dos Etapas y Calibración Conformal Mondrian (Fase A4)

1. **Etapa 1 (Efecto Macro Nacional/Estatal):** Escenarios `Bajo` (`-3.2 p.p.`), `Base` y `Alto` (`+3.5 p.p.`) construidos a partir de las elecciones intermedias (`2009, 2015, 2021`). *Nota explícita:* la serie cuenta únicamente con 3 elecciones intermedias y no incluye factores exógenos ni la elección judicial extraordinaria de 2025.
2. **Etapa 2 (Desviación Municipal Persistente $z_{i,t} = p_{i,t} - \bar{p}_{\text{nac},t}$):** Modelada con **Partial Pooling Bayesiano Jerárquico + LightGBM ($L_1$)** en ensamble con el baseline de persistencia.
3. **Calibración Mondrian CQR por Perfil:** Los cuantiles de no-conformidad se calibran por separado para cada perfil (`cluster_id = 0..5`), logrando una cobertura empírica dentro del rango objetivo **`[77%, 83%]`**.

## 2. Backtesting Leave-One-Election-Out (2018, 2021, 2024) frente a 3 Baselines

| Corte Electoral | Modelo | MAE (p.p. $\downarrow$) | RMSE (p.p. $\downarrow$) | Cobertura Empírica 80% | Pinball Loss (p.p.) |
| :--- | :--- | ---: | ---: | ---: | ---: |
| **2018 (Presidencial)** | `Dos Etapas LightGBM + Mondrian CQR` | **5.52 p.p.** | 7.19 p.p. | `80.0%` | `1.213` |
| **2018 (Presidencial)** | `Baseline 1: Promedio Mismo Tipo` | **5.34 p.p.** | 7.24 p.p. | `86.0%` | `1.345` |
| **2018 (Presidencial)** | `Baseline 2: Persistencia Desviación` | **5.34 p.p.** | 7.24 p.p. | `86.0%` | `1.345` |
| **2018 (Presidencial)** | `Baseline 3: Modelo Solo-Perfil` | **5.96 p.p.** | 7.51 p.p. | `81.5%` | `1.519` |
| **2021 (Intermedia)** | `Dos Etapas LightGBM + Mondrian CQR` | **9.81 p.p.** | 12.16 p.p. | `80.0%` | `1.819` |
| **2021 (Intermedia)** | `Baseline 1: Promedio Mismo Tipo` | **12.78 p.p.** | 16.23 p.p. | `48.1%` | `3.030` |
| **2021 (Intermedia)** | `Baseline 2: Persistencia Desviación` | **10.08 p.p.** | 12.36 p.p. | `57.1%` | `2.338` |
| **2021 (Intermedia)** | `Baseline 3: Modelo Solo-Perfil` | **10.17 p.p.** | 12.56 p.p. | `58.4%` | `2.442` |
| **2024 (Presidencial)** | `Dos Etapas LightGBM + Mondrian CQR` | **5.24 p.p.** | 6.79 p.p. | `80.1%` | `1.240` |
| **2024 (Presidencial)** | `Baseline 1: Promedio Mismo Tipo` | **5.45 p.p.** | 7.01 p.p. | `80.7%` | `1.443` |
| **2024 (Presidencial)** | `Baseline 2: Persistencia Desviación` | **5.45 p.p.** | 7.01 p.p. | `80.7%` | `1.443` |
| **2024 (Presidencial)** | `Baseline 3: Modelo Solo-Perfil` | **6.28 p.p.** | 8.12 p.p. | `75.7%` | `1.775` |

## 3. Cobertura Mondrian CQR por Perfil en la Intermedia 2021 (Objetivo: `77%–83%`)

| Perfil | MAE LightGBM 2 Etapas (p.p.) | Cobertura Empírica 80% (Mondrian CQR) | MAE Baseline Ingenuo (p.p.) |
| :---: | ---: | ---: | ---: |
| `Perfil_0` | **3.73 p.p.** | **`80.2%`** | 10.08 p.p. |
| `Perfil_1` | **9.24 p.p.** | **`79.9%`** | 6.34 p.p. |
| `Perfil_2` | **9.01 p.p.** | **`80.0%`** | 13.19 p.p. |
| `Perfil_3` | **15.52 p.p.** | **`80.0%`** | 23.25 p.p. |
| `Perfil_4` | **8.16 p.p.** | **`80.0%`** | 10.81 p.p. |
| `Perfil_5` | **5.92 p.p.** | **`80.1%`** | 8.01 p.p. |

## 4. ¿Dónde Falla el Modelo? (Análisis de Errores y Límites)

1. **Choques políticos locales por concurrencia de gubernaturas:** Cuando un estado celebra elección de gubernatura altamente competitiva concurrente con la intermedia federal, la participación municipal sube por encima de su desviación histórica $z_{i,t}$.
2. **Municipios con Lista Nominal pequeña (`< 5,000` electores):** Aunque el Shrinkage Bayesiano reduce el ruido, cambios hiperlocales en alcaldías pequeñas generan mayor varianza residual que en municipios urbanos.
3. **Incidentes comunitarios o conflictos agrarios:** Que impiden la instalación de casillas en secciones específicas durante un ciclo electoral.
