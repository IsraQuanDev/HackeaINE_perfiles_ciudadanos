# Reporte de Segmentación Territorial v2 — Ensemble por Consenso (`docs/segmentacion.md`)

> **Principio metodológico (Falacia Ecológica):** Los perfiles obtenidos describen **territorios municipales (`cve_geo`)** según su comportamiento electoral agregado 2009–2024, y bajo ninguna circunstancia deben interpretarse como atributos psicológicos o individuales de las personas residentes.

## 1. Impacto de la Limpieza de Ceros Falsos (`NS`) y Shrinkage Bayesiano (`v2` vs. `v1-baseline`)

- **Municipios que cambiaron de perfil tras reparar ceros espurios (`NS == LN`) y aplicar Shrinkage Beta-Binomial:** `1962` municipios (`79.2%` del total; ARI entre v1 y v2 = `0.2209`).
- **Diagnóstico del antiguo perfil «Dinámica Local Volátil» (P0-5):** En `v1-baseline`, los municipios con `NS == LN` (como *Atil, Higueras, Oquitoa, Cucurpe, Tubutama* en 2024 o *Rayones, Magdalena Ocotlán* en 2009) presentaban volatilidades artificiales de ~30 p.p. Al aplicar `cobertura < 0.90 -> NA` y Shrinkage Bayesiano, la volatilidad media de esos 7 municipios cayó de **`29.7 p.p.`** a **`4.8 p.p.`**, eliminando por completo el artefacto de ceros falsos.

## 2. Enfoques Comparados y Variables de Segmentación v2

Evaluados sobre `N = 2,477` municipios con ponderación por Lista Nominal ($\log(1 + \text{LN})$) y escalado `RobustScaler`:

- `part_media_global`
- `caida_presidencial_intermedia`
- `pendiente_tendencia`
- `volatilidad`
- `constancia_sobre_mediana`
- `brecha_genero_media`
- `brecha_juvenil_18_29_vs_30_59`
- `retencion_primer_voto`
- `pct_ln_rural`
- `rezago_espacial_part`

## 3. Validación Cuantitativa para $k \in [3..10]$ y Comparación de Enfoques (A, B, C, D, E, F)

| Método / Enfoque | $k$ | Silhouette ($\uparrow$) | Davies-Bouldin ($\downarrow$) | Calinski-Harabasz ($\uparrow$) | Estabilidad Bootstrap ARI ($n=100, \uparrow$) | Tamaño Mín. de Cluster ($\% \ge 3\%$) | BIC |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `A_KMeans_Robust` | 3 | 0.1753 | 1.8170 | 523.5 | 0.9656 | 28.74% | N/A |
| `B_GMM_BIC` | 3 | 0.1165 | 2.4368 | 336.1 | 0.4545 | 20.10% | 43,157 |
| `A_KMeans_Robust` | 4 | 0.1657 | 1.8118 | 453.4 | 0.8625 | 19.10% | N/A |
| `B_GMM_BIC` | 4 | 0.0596 | 3.9389 | 202.7 | 0.4021 | 17.48% | 37,131 |
| `A_KMeans_Robust` | 5 | 0.1561 | 1.6945 | 423.2 | 0.8210 | 11.38% | N/A |
| `B_GMM_BIC` | 5 | 0.0366 | 3.9753 | 165.4 | 0.4540 | 4.56% | 32,680 |
| `A_KMeans_Robust` | 6 | 0.1716 | 1.5898 | 396.5 | 0.8059 | 4.48% | N/A |
| `B_GMM_BIC` | 6 | 0.0293 | 4.1322 | 178.3 | 0.5685 | 4.16% | 32,335 |
| `A_KMeans_Robust` | 7 | 0.1575 | 1.6723 | 369.7 | 0.6307 | 4.68% | N/A |
| `B_GMM_BIC` | 7 | 0.0025 | 3.9235 | 158.3 | 0.7044 | 5.53% | 32,302 |
| `A_KMeans_Robust` | 8 | 0.1496 | 1.6541 | 347.0 | 0.5522 | 4.28% | N/A |
| `B_GMM_BIC` | 8 | 0.0152 | 3.2812 | 169.2 | 0.5377 | 3.75% | 31,985 |
| `A_KMeans_Robust` | 9 | 0.1410 | 1.6457 | 328.9 | 0.5617 | 4.32% | N/A |
| `B_GMM_BIC` | 9 | 0.0064 | 3.6857 | 151.5 | 0.5347 | 2.91% | 32,190 |
| `A_KMeans_Robust` | 10 | 0.1377 | 1.6324 | 316.3 | 0.7171 | 4.16% | N/A |
| `B_GMM_BIC` | 10 | -0.0143 | 3.1399 | 129.1 | 0.6078 | 1.98% | 31,259 |
| `D_DTW_Trayectorias` | 5 | 0.0636 | 3.3792 | 228.2 | 0.8500 | 9.12% | N/A |
| `D_DTW_Trayectorias` | 6 | 0.0519 | 3.5751 | 194.2 | 0.8500 | 8.52% | N/A |
| `E_Espacial_Contiguo` | 6 | 0.0456 | 2.7551 | 183.6 | 0.8000 | 4.32% | N/A |
| `F_Ensemble_Consenso_LN` | 6 | 0.1716 | 1.5902 | 396.4 | 0.9011 | 4.48% | N/A |
| `C_HDBSCAN (min_cluster=45)` | 2 (+38.1% ruido) | 0.3372 | 0.8336 | 185.6 | N/A (densidad) | N/A | N/A |

## 4. Selección del Modelo Ganador y Municipios Prototipo Reales (Medoides)

- **Modelo ganador seleccionado:** `F_Ensemble_Consenso_LN` con **$k = 6$ perfiles territoriales**.
- **Sensibilidad al escalado (`RobustScaler` vs `StandardScaler`, ARI):** `0.5987`.
- **Sensibilidad al subconjunto de features (ARI):** `0.5533`.

### Caracterización Cuantitativa y Municipio Prototipo Real (Medoide) por Perfil

| Cluster | Municipios ($N$) | % Municipios | Part. Media Global | Caída Pres $\rightarrow$ Inter | Pendiente (p.p./ciclo) | Brecha Juvenil (18-29 vs 30-59) | Retención 1er Voto | Municipio Prototipo Real (Medoide) |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| **Perfil 0** | 111 | 4.5% | 79.3% | +12.2 p.p. | +2.58 p.p. | -6.4 p.p. | 98.4% | **Baca, Yucatán** (`31004`) |
| **Perfil 1** | 537 | 21.7% | 65.1% | +4.5 p.p. | +0.18 p.p. | -7.6 p.p. | 88.0% | **Mazamitla, Jalisco** (`14061`) |
| **Perfil 2** | 425 | 17.2% | 61.8% | +8.2 p.p. | +1.36 p.p. | -16.6 p.p. | 87.0% | **Altotonga, Veracruz** (`30011`) |
| **Perfil 3** | 554 | 22.4% | 58.0% | +18.3 p.p. | +5.97 p.p. | -10.5 p.p. | 91.5% | **Oriental, Puebla** (`21109`) |
| **Perfil 4** | 659 | 26.6% | 50.0% | +13.6 p.p. | +1.72 p.p. | -11.6 p.p. | 82.0% | **La Antigua, Veracruz** (`30017`) |
| **Perfil 5** | 191 | 7.7% | 49.8% | +12.1 p.p. | +1.36 p.p. | -19.1 p.p. | 104.7% | **San Pedro Molinos, Oaxaca** (`20318`) |
