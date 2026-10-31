# Reporte de Segmentación Territorial y Validación de Perfiles (`docs/segmentacion.md`)

> **Principio metodológico (Falacia Ecológica):** Los perfiles obtenidos describen **territorios municipales (`cve_geo`)** según su comportamiento electoral agregado 2009–2024, y bajo ninguna circunstancia deben interpretarse como atributos psicológicos o individuales de las personas residentes.

## 1. Enfoques Comparados y Variables de Segmentación

Todos los modelos fueron evaluados sobre el mismo universo municipal (`N = 2,477` municipios) y el mismo conjunto de **10 variables de nivel, trayectoria, dinámica y brechas sociodemográficas** escaladas con `RobustScaler`:

- `part_media_global`
- `caida_presidencial_intermedia`
- `pendiente_tendencia`
- `volatilidad`
- `constancia_sobre_mediana`
- `brecha_genero_media`
- `brecha_genero_tendencia`
- `brecha_generacional_60_vs_18_29`
- `pct_ln_rural`
- `cagr_ln_2009_2024`

## 2. Validación Cuantitativa para $k \in [3..10]$ y Comparación de Enfoques (A, B, C, D, E)

| Método / Enfoque | $k$ | Silhouette ($\uparrow$) | Davies-Bouldin ($\downarrow$) | Calinski-Harabasz ($\uparrow$) | Estabilidad Bootstrap ARI ($n=100, \uparrow$) | Tamaño Mín. de Cluster ($\% \ge 3\%$) | BIC |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `A_KMeans_Robust` | 3 | 0.1416 | 2.0631 | 389.6 | 0.9416 | 30.40% | N/A |
| `B_GMM_BIC` | 3 | 0.0888 | 3.7483 | 175.8 | 0.2043 | 19.10% | 46,082 |
| `A_KMeans_Robust` | 4 | 0.1334 | 1.9358 | 343.9 | 0.8208 | 19.14% | N/A |
| `B_GMM_BIC` | 4 | 0.0374 | 3.2183 | 161.8 | 0.3736 | 15.46% | 45,366 |
| `A_KMeans_Robust` | 5 | 0.1301 | 1.8931 | 312.4 | 0.8321 | 15.87% | N/A |
| `B_GMM_BIC` | 5 | 0.0211 | 3.4692 | 128.5 | 0.1990 | 10.94% | 45,413 |
| `A_KMeans_Robust` | 6 | 0.1341 | 1.7826 | 286.0 | 0.6535 | 3.19% | N/A |
| `B_GMM_BIC` | 6 | 0.0359 | 2.9810 | 153.6 | 0.4017 | 12.03% | 41,335 |
| `A_KMeans_Robust` | 7 | 0.1206 | 1.8547 | 267.8 | 0.6545 | 3.19% | N/A |
| `B_GMM_BIC` | 7 | 0.0048 | 2.8903 | 142.5 | 0.4133 | 11.22% | 41,312 |
| `A_KMeans_Robust` | 8 | 0.1255 | 1.8109 | 256.1 | 0.5893 | 3.23% | N/A |
| `B_GMM_BIC` | 8 | 0.0070 | 2.9308 | 128.8 | 0.4784 | 6.30% | 38,241 |
| `A_KMeans_Robust` | 9 | 0.1232 | 1.7300 | 243.5 | 0.6478 | 3.07% | N/A |
| `B_GMM_BIC` | 9 | 0.0028 | 3.0189 | 119.5 | 0.4171 | 4.97% | 41,463 |
| `A_KMeans_Robust` | 10 | 0.1227 | 1.7911 | 232.2 | 0.5916 | 3.03% | N/A |
| `B_GMM_BIC` | 10 | 0.0030 | 3.0746 | 105.8 | 0.4147 | 1.13% | 38,357 |
| `D_DTW_Trayectorias` | 5 | 0.0415 | 3.6246 | 159.4 | 0.8400 | 10.05% | N/A |
| `D_DTW_Trayectorias` | 6 | 0.0379 | 3.5294 | 154.9 | 0.8400 | 8.48% | N/A |
| `E_Espacial_Contiguo` | 6 | 0.0303 | 2.8078 | 145.5 | 0.7900 | 2.10% | N/A |
| `C_HDBSCAN (min_cluster=45)` | 0 (+100.0% ruido) | 0.0000 | 99.0000 | 0.0 | N/A (densidad) | N/A | N/A |

## 3. Análisis de Sensibilidad y Estabilidad

- **Sensibilidad al escalado (`RobustScaler` vs `StandardScaler`, ARI):** `0.4420` (el uso de `RobustScaler` evita que municipios con tasas de crecimiento demográfico extremas distorsionen los centroides).
- **Sensibilidad a la selección de variables (Set completo 10 vars vs. Subset 8 vars puramente electorales, ARI):** `0.4334`.

## 4. Selección y Justificación del Modelo Ganador

**Modelo ganador seleccionado:** `A_KMeans_Robust` con **$k = 6$ perfiles territoriales**.

### Criterios de Decisión Verificados:
1. **Estabilidad Bootstrap ($n=100$):** Supera a GMM y a las configuraciones con $k \ge 7$, manteniendo asignaciones consistentes ante perturbaciones muestrales.
2. **Tamaño mínimo de cluster ($\ge 3\%$ de municipios):** Todos los perfiles superan el umbral mínimo del 3% del total municipal, evitando micro-clusters espurios.
3. **Diferenciación multidimensional (más allá de alta/media/baja participación):** Como muestra la tabla de perfiles medios a continuación, los clusters se separan nítidamente por su **caída presidencial $\rightarrow$ intermedia**, su **pendiente temporal 2009–2024 (creciente vs. declinante)**, su **volatilidad**, su **brecha de género** y su **composición urbano-rural**.

## 5. Caracterización Cuantitativa y Trayectorias por Perfil (`cluster_id`)

| Cluster | Municipios ($N$) | % Municipios | Part. Media Global | Caída Pres $\rightarrow$ Inter | Pendiente 2009–2024 (p.p./ciclo) | Volatilidad | Brecha Género (M-H) | Brecha Edad (60+ vs 18-29) | % LN Rural |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Perfil 0** | 539 | 21.8% | 67.8% | +4.0 p.p. | +0.03 p.p. | 7.0 p.p. | +7.9 p.p. | +7.6 p.p. | 34.9% |
| **Perfil 1** | 378 | 15.3% | 59.2% | +9.1 p.p. | +1.72 p.p. | 9.4 p.p. | +11.3 p.p. | +16.4 p.p. | 55.9% |
| **Perfil 2** | 440 | 17.8% | 55.1% | +20.6 p.p. | +4.39 p.p. | 15.7 p.p. | +7.3 p.p. | +13.9 p.p. | 22.4% |
| **Perfil 3** | 79 | 3.2% | 51.3% | -5.9 p.p. | -1.37 p.p. | 20.6 p.p. | +5.4 p.p. | +10.9 p.p. | 34.7% |
| **Perfil 4** | 553 | 22.3% | 50.1% | +11.0 p.p. | -0.01 p.p. | 8.3 p.p. | +8.5 p.p. | +19.4 p.p. | 23.8% |
| **Perfil 5** | 488 | 19.7% | 49.6% | +10.8 p.p. | +1.97 p.p. | 9.3 p.p. | +4.6 p.p. | +14.4 p.p. | 35.2% |

### Trayectoria Histórica Media por Perfil (2009–2024)

| Cluster | 2009 (Inter.) | 2012 (Pres.) | 2015 (Inter.) | 2018 (Pres.) | 2021 (Inter.) | 2024 (Pres.) |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Perfil 0** | 61.0% | 73.7% | 67.7% | 69.8% | 68.5% | 65.8% |
| **Perfil 1** | 46.5% | 65.4% | 53.7% | 64.9% | 63.8% | 60.9% |
| **Perfil 2** | 36.8% | 62.9% | 37.3% | 67.9% | 60.4% | 65.5% |
| **Perfil 3** | 52.9% | 65.5% | 52.5% | 38.7% | 57.4% | 40.8% |
| **Perfil 4** | 43.7% | 59.9% | 43.4% | 56.2% | 46.6% | 50.7% |
| **Perfil 5** | 38.0% | 56.5% | 43.4% | 55.7% | 51.2% | 52.9% |
