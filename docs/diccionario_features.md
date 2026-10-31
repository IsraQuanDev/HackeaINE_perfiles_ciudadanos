# Diccionario de Variables (`features_municipio.parquet`)

Unidad de análisis: **Municipio (`cve_geo`, 5 dígitos: `cve_ent` + `cve_mun`)**, periodo **2009–2024** (6 elecciones federales: 3 intermedias y 3 presidenciales).

## 1. Identificadores y Metadatos de Confiabilidad / Marco Geográfico

| Nombre de Variable | Definición | Fórmula / Regla | Unidad / Tipo |
| :--- | :--- | :--- | :--- |
| `cve_geo` | Clave geoestadística/electoral única del municipio (concatenación de entidad y municipio INE). | `LPAD(EDOCVE, 2, '0') || LPAD(MPIOCVE, 3, '0')` | `string` (5 dígitos) |
| `cve_ent` | Clave INE de Entidad Federativa. | `LPAD(EDOCVE, 2, '0')` | `string` (`'01'`..`'32'`) |
| `nom_ent` | Nombre oficial estandarizado de la Entidad Federativa. | Catálogo INE 32 entidades | `string` |
| `cve_mun` | Clave INE de Municipio dentro de la entidad. | `LPAD(MPIOCVE, 3, '0')` | `string` (3 dígitos) |
| `nom_mun` | Nombre del Municipio registrado en el Conteo Censal más reciente. | `LAST(MPIONOM)` | `string` |
| `def_principal` | Distrito Electoral Federal predominante del municipio por Lista Nominal. | $\arg\max_{d} \sum LN_{m,d}$ | `string` |
| `n_elecciones_observadas` | Número de elecciones federales en las que el municipio existió y registró conteo censal. | $\sum_{t \in \{2009..2024\}} \mathbb{I}(LN_{m,t} > 0)$ | `int` ($1..6$) |
| `flag_imputacion_trayectoria` | Bandera que indica si se imputó algún año faltante (por creación reciente del municipio) con la mediana estatal de ese año. | `n_elecciones_observadas < 6` | `bool` |
| `flag_baja_confiabilidad` | Bandera para municipios con padrón pequeño o serie incompleta donde las tasas exhiben mayor varianza muestral. | `ln_promedio < 1000 OR n_elecciones_observadas < 6` | `bool` |
| `estatus_marco_geografico` | Clasificación en la tabla puente `puente_municipio_anio`. | `ESTABLE_2009_2024` / `NUEVA_CREACION_YYYY` | `string` |

---

## 2. Serie Temporal y Niveles de Participación Electoral

| Nombre de Variable | Definición | Fórmula | Unidad |
| :--- | :--- | :--- | :--- |
| `part_2009` .. `part_2024` | Tasa de participación municipal en cada elección federal (con imputación por mediana estatal documentada cuando el municipio aún no había sido creado). | $P_{m,t} = \frac{SV_{m,t}}{LN_{m,t}}$ | Proporción $[0, 1]$ |
| `part_2009_raw` .. `part_2024_raw` | Tasa de participación municipal observada sin imputación (`NaN` si el municipio no existía en el año $t$). | $P^{\text{raw}}_{m,t} = \frac{SV_{m,t}}{LN_{m,t}}$ | Proporción $[0, 1]$ |
| `part_media_global` | Promedio histórico de participación en las 6 elecciones federales (2009–2024). | $\bar{P}_m = \frac{1}{6}\sum_{t} P_{m,t}$ | Proporción $[0, 1]$ |
| `part_media_presidencial` | Promedio de participación en elecciones presidenciales (2012, 2018, 2024). | $\bar{P}^{\text{pres}}_m = \frac{P_{2012} + P_{2018} + P_{2024}}{3}$ | Proporción $[0, 1]$ |
| `part_media_intermedia` | Promedio de participación en elecciones intermedias (2009, 2015, 2021). | $\bar{P}^{\text{inter}}_m = \frac{P_{2009} + P_{2015} + P_{2021}}{3}$ | Proporción $[0, 1]$ |
| `caida_presidencial_intermedia` | Brecha estructural entre elecciones presidenciales e intermedias. | $\Delta^{\text{pres-inter}}_m = \bar{P}^{\text{pres}}_m - \bar{P}^{\text{inter}}_m$ | Diferencia en proporción $[-1, 1]$ |
| `pendiente_tendencia` | Pendiente de tendencia temporal 2009–2024 estimada mediante regresión robusta de Theil-Sen sobre los ciclos observados $k \in \{0..5\}$. | $\text{mediana}_{i < j} \left(\frac{P_{m,k_j} - P_{m,k_i}}{k_j - k_i}\right)$ | Cambio en proporción / ciclo electoral |
| `volatilidad` | Desviación estándar inter-elección de la tasa de participación del municipio. | $\sigma_m = \sqrt{\frac{1}{T}\sum_t (P_{m,t} - \bar{P}_m)^2}$ | Proporción $[0, 1]$ |
| `volatilidad_intra_tipo` | Volatilidad promedio controlando por el efecto presidencial vs. intermedia. | $\frac{1}{2}(\sigma(P^{\text{pres}}_m) + \sigma(P^{\text{inter}}_m))$ | Proporción $[0, 1]$ |
| `constancia_sobre_mediana` | Proporción de elecciones en las que la participación del municipio superó la mediana municipal nacional de ese mismo año. | $\frac{1}{T_m}\sum_{t} \mathbb{I}\left(P_{m,t} > \text{mediana}_t(P_{\cdot,t})\right)$ | Proporción $[0, 1]$ |
| `serie_temporal_json` | Vector serializado JSON `[p_2009, p_2012, p_2015, p_2018, p_2021, p_2024]`. | Vector de longitud 6 | `string` (JSON) |

---

## 3. Brechas de Género, Estructura Etaria y Urbanización Electoral (CCPC INE)

| Nombre de Variable | Definición | Fórmula | Unidad |
| :--- | :--- | :--- | :--- |
| `brecha_genero_media` | Diferencia media entre la tasa de participación de mujeres (`SEXO=1`) y hombres (`SEXO=0`). | $\frac{1}{T_m}\sum_t (P^{\text{mujeres}}_{m,t} - P^{\text{hombres}}_{m,t})$ | Diferencia en proporción $[-1, 1]$ |
| `brecha_genero_tendencia` | Pendiente Theil-Sen de la evolución de la brecha de género entre 2009 y 2024. | $\text{TheilSen}(P^{\text{M}}_{m,t} - P^{\text{H}}_{m,t})$ | Cambio en proporción / ciclo |
| `pct_ln_jovenes_18_29` | Proporción de la Lista Nominal municipal correspondiente a jóvenes de 18 a 29 años. | $\frac{\sum_t LN_{m,t,\text{18-29}}}{\sum_t LN_{m,t}}$ | Proporción $[0, 1]$ |
| `pct_ln_adultos_60_mas` | Proporción de la Lista Nominal municipal correspondiente a personas de 60 años o más. | $\frac{\sum_t LN_{m,t,\text{60+}}}{\sum_t LN_{m,t}}$ | Proporción $[0, 1]$ |
| `part_media_jovenes_18_29` | Tasa media de participación del grupo juvenil (18–29 años). | $\frac{1}{T_m}\sum_t \frac{SV_{m,t,\text{18-29}}}{LN_{m,t,\text{18-29}}}$ | Proporción $[0, 1]$ |
| `part_media_adultos_30_59` | Tasa media de participación del grupo adulto (30–59 años). | $\frac{1}{T_m}\sum_t \frac{SV_{m,t,\text{30-59}}}{LN_{m,t,\text{30-59}}}$ | Proporción $[0, 1]$ |
| `part_media_adultos_60_mas` | Tasa media de participación de personas adultas mayores (60+ años). | $\frac{1}{T_m}\sum_t \frac{SV_{m,t,\text{60+}}}{LN_{m,t,\text{60+}}}$ | Proporción $[0, 1]$ |
| `brecha_generacional_60_vs_18_29` | Diferencia media de participación entre adultos mayores (60+) y jóvenes (18–29). | $\frac{1}{T_m}\sum_t (P^{\text{60+}}_{m,t} - P^{\text{18-29}}_{m,t})$ | Diferencia en proporción $[-1, 1]$ |
| `pct_ln_urbana` | Proporción de la Lista Nominal ubicada en secciones electorales Urbanas (`TIPOSEC='U'`). | $\frac{\sum_t LN_{m,t,U}}{\sum_t LN_{m,t}}$ | Proporción $[0, 1]$ |
| `pct_ln_mixta` | Proporción de la Lista Nominal ubicada en secciones electorales Mixtas (`TIPOSEC='M'`). | $\frac{\sum_t LN_{m,t,M}}{\sum_t LN_{m,t}}$ | Proporción $[0, 1]$ |
| `pct_ln_rural` | Proporción de la Lista Nominal ubicada en secciones electorales Rurales (`TIPOSEC='R'`). | $\frac{\sum_t LN_{m,t,R}}{\sum_t LN_{m,t}}$ | Proporción $[0, 1]$ |

---

## 4. Dinámica del Padrón, Voto Anticipado 2024 y Autocorrelación Espacial

| Nombre de Variable | Definición | Fórmula | Unidad |
| :--- | :--- | :--- | :--- |
| `ln_2009`, `ln_2024`, `ln_promedio` | Lista nominal inicial, final (2024) y promedio histórico del municipio. | Conteo de electores en cuadernillos | Personas (entero / flotante) |
| `crecimiento_ln_relativo` | Crecimiento acumulado relativo de la lista nominal entre la primera y última elección observada. | $\frac{LN_{m,2024} - LN_{m,t_0}}{LN_{m,t_0}}$ | Razón relativa |
| `cagr_ln_2009_2024` | Tasa de crecimiento anual compuesta (CAGR) de la lista nominal municipal. | $\left(\frac{LN_{m,2024}}{LN_{m,t_0}}\right)^{\frac{1}{2024-t_0}} - 1$ | Tasa anual |
| `votantes_anticipado_2024` | Personas votantes bajo modalidad de Voto Anticipado en 2024 en el municipio. | Conteo de registros en `VotoAnticipado2024` | Personas (`int`) |
| `tasa_voto_anticipado_por_10k` | Tasa de adopción del Voto Anticipado en 2024 por cada 10,000 integrantes de la Lista Nominal. | $\frac{\text{votantes\_anticipado\_2024} \times 10000}{LN_{m,2024}}$ | Votantes / 10,000 LN |
| `moran_global_i` | Estadístico $I$ de Moran Global de autocorrelación espacial de `part_media_global`. | $I = \frac{N}{W}\frac{\sum_i \sum_j w_{ij}(y_i - \bar{y})(y_j - \bar{y})}{\sum_i (y_i - \bar{y})^2}$ | Escalado $[-1, 1]$ |
| `lisa_i`, `lisa_p_val`, `lisa_cluster` | Indicador Local de Asociación Espacial (LISA) y tipología de cluster (`HH`, `LL`, `HL`, `LH`, `NS`). | $I_i = z_i \sum_j w_{ij} z_j$ ($p < 0.05$, 499 permutaciones) | Estadístico / Categoría |
