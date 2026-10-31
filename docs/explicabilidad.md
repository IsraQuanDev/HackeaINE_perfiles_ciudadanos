# Explicabilidad de Perfiles y Dinámica Territorial (`docs/explicabilidad.md`)

## 1. Modelos Sustitutos de Explicabilidad Global (Árbol de Decisión + LightGBM SHAP)

- **Exactitud del Árbol de Decisión interpretable (`max_depth=3`):** `67.02%`
- **Exactitud del modelo LightGBM + TreeExplainer SHAP:** `100.00%`

### Ranking Global de Importancia SHAP (`mean(|SHAP|)`)

| Orden | Variable | Importancia Media Absoluta SHAP |
| :---: | :--- | ---: |
| 1 | `volatilidad` | `0.83060` |
| 2 | `part_media_global` | `0.74205` |
| 3 | `brecha_genero_tendencia` | `0.72089` |
| 4 | `brecha_genero_media` | `0.70519` |
| 5 | `caida_presidencial_intermedia` | `0.61024` |
| 6 | `brecha_generacional_60_vs_18_29` | `0.54438` |
| 7 | `cagr_ln_2009_2024` | `0.53605` |
| 8 | `pendiente_tendencia` | `0.52186` |
| 9 | `constancia_sobre_mediana` | `0.22677` |
| 10 | `pct_ln_rural` | `0.22471` |

### Reglas del Árbol de Decisión de Poca Profundidad (`max_depth=3`)

```text
|--- part_media_global <= 0.61
|   |--- volatilidad <= 0.12
|   |   |--- cagr_ln_2009_2024 <= 0.01
|   |   |   |--- class: 5
|   |   |--- cagr_ln_2009_2024 >  0.01
|   |   |   |--- class: 4
|   |--- volatilidad >  0.12
|   |   |--- caida_presidencial_intermedia <= 0.09
|   |   |   |--- class: 3
|   |   |--- caida_presidencial_intermedia >  0.09
|   |   |   |--- class: 2
|--- part_media_global >  0.61
|   |--- brecha_genero_tendencia <= 0.01
|   |   |--- caida_presidencial_intermedia <= 0.15
|   |   |   |--- class: 0
|   |   |--- caida_presidencial_intermedia >  0.15
|   |   |   |--- class: 2
|   |--- brecha_genero_tendencia >  0.01
|   |   |--- brecha_generacional_60_vs_18_29 <= 0.05
|   |   |   |--- class: 0
|   |   |--- brecha_generacional_60_vs_18_29 >  0.05
|   |   |   |--- class: 1
```

---

## 2. Variables Definitorias (SHAP) y Municipios Representativos por Perfil

### Perfil 0 (539 municipios — 21.76% del total; Lista Nominal 2024: 8,089,025)

**Top 5 variables que definen el perfil (SHAP por cluster):**

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `part_media_global` | `2.8674` | `0.6776` | `0.5616` | `+1.13` | ALTA (+) |
| `brecha_generacional_60_vs_18_29` | `1.8286` | `0.0757` | `0.1413` | `-0.87` | BAJA (-) |
| `caida_presidencial_intermedia` | `1.2553` | `0.0404` | `0.1032` | `-0.75` | BAJA (-) |
| `volatilidad` | `0.7387` | `0.0701` | `0.1011` | `-0.65` | BAJA (-) |
| `constancia_sobre_mediana` | `0.7320` | `0.8568` | `0.4991` | `+1.02` | ALTA (+) |

- **Entidades predominantes:** JALISCO (95 muns, 17.63%), YUCATAN (90 muns, 16.7%), ESTADO DE MEXICO (70 muns, 12.99%), SONORA (37 muns, 6.86%), SAN LUIS POTOSI (35 muns, 6.49%)
- **Municipios más representativos (cercanos al centroide):** GÃ³mez FarÃ­as (TAMAULIPAS, `cve_geo=28011`, part=66.75%), Mazamitla (JALISCO, `cve_geo=14061`, part=65.17%), ChiquilistlÃ¡n (JALISCO, `cve_geo=14033`, part=66.19%), Tlayacapan (MORELOS, `cve_geo=17026`, part=68.69%), Tetecala (MORELOS, `cve_geo=17021`, part=70.72%)

### Perfil 1 (378 municipios — 15.26% del total; Lista Nominal 2024: 6,851,597)

**Top 5 variables que definen el perfil (SHAP por cluster):**

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `brecha_genero_tendencia` | `3.5810` | `0.0144` | `0.0046` | `+1.14` | ALTA (+) |
| `brecha_genero_media` | `2.5505` | `0.1135` | `0.0772` | `+1.01` | ALTA (+) |
| `pct_ln_rural` | `1.0539` | `0.5592` | `0.3345` | `+0.80` | ALTA (+) |
| `part_media_global` | `0.7611` | `0.5920` | `0.5616` | `+0.30` | ALTA (+) |
| `brecha_generacional_60_vs_18_29` | `0.2893` | `0.1639` | `0.1413` | `+0.30` | ALTA (+) |

- **Entidades predominantes:** OAXACA (67 muns, 17.72%), PUEBLA (50 muns, 13.23%), CHIAPAS (43 muns, 11.38%), VERACRUZ (42 muns, 11.11%), GUERRERO (36 muns, 9.52%)
- **Municipios más representativos (cercanos al centroide):** Charo (MICHOACAN, `cve_geo=16022`, part=55.35%), OlinalÃ¡ (GUERRERO, `cve_geo=12046`, part=63.09%), CacahoatÃ¡n (CHIAPAS, `cve_geo=07015`, part=58.82%), Noria de Ãngeles (ZACATECAS, `cve_geo=32035`, part=59.37%), CoxcatlÃ¡n (PUEBLA, `cve_geo=21036`, part=55.5%)

### Perfil 2 (440 municipios — 17.76% del total; Lista Nominal 2024: 13,283,697)

**Top 5 variables que definen el perfil (SHAP por cluster):**

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `volatilidad` | `4.1284` | `0.1573` | `0.1011` | `+1.18` | ALTA (+) |
| `caida_presidencial_intermedia` | `2.5286` | `0.2063` | `0.1032` | `+1.22` | ALTA (+) |
| `pendiente_tendencia` | `2.1273` | `0.0439` | `0.0139` | `+1.03` | ALTA (+) |
| `pct_ln_rural` | `0.2169` | `0.2239` | `0.3345` | `-0.39` | BAJA (-) |
| `brecha_genero_tendencia` | `0.1568` | `0.0065` | `0.0046` | `+0.22` | ALTA (+) |

- **Entidades predominantes:** OAXACA (132 muns, 30.0%), PUEBLA (124 muns, 28.18%), TLAXCALA (46 muns, 10.45%), CHIAPAS (28 muns, 6.36%), HIDALGO (17 muns, 3.86%)
- **Municipios más representativos (cercanos al centroide):** San Pedro y San Pablo Teposcolula (OAXACA, `cve_geo=20334`, part=57.46%), Villa de TamazulÃ¡pam del Progreso (OAXACA, `cve_geo=20539`, part=57.42%), Xaloztoc (TLAXCALA, `cve_geo=29039`, part=53.66%), Zacatelco (TLAXCALA, `cve_geo=29044`, part=55.09%), TeotitlÃ¡n de Flores MagÃ³n (OAXACA, `cve_geo=20545`, part=58.15%)

### Perfil 3 (79 municipios — 3.19% del total; Lista Nominal 2024: 715,243)

**Top 5 variables que definen el perfil (SHAP por cluster):**

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `volatilidad` | `6.6823` | `0.2063` | `0.1011` | `+2.21` | ALTA (+) |
| `caida_presidencial_intermedia` | `5.7545` | `-0.0593` | `0.1032` | `-1.93` | BAJA (-) |
| `pendiente_tendencia` | `0.9997` | `-0.0137` | `0.0139` | `-0.95` | BAJA (-) |
| `brecha_genero_media` | `0.9719` | `0.0540` | `0.0772` | `-0.64` | BAJA (-) |
| `brecha_genero_tendencia` | `0.4340` | `-0.0006` | `0.0046` | `-0.60` | BAJA (-) |

- **Entidades predominantes:** OAXACA (21 muns, 26.58%), CHIAPAS (10 muns, 12.66%), SONORA (10 muns, 12.66%), HIDALGO (7 muns, 8.86%), VERACRUZ (6 muns, 7.59%)
- **Municipios más representativos (cercanos al centroide):** AmatitlÃ¡n (VERACRUZ, `cve_geo=30013`, part=52.53%), San Bartolo Tutotepec (HIDALGO, `cve_geo=13052`, part=49.38%), Santo Domingo Tehuantepec (OAXACA, `cve_geo=20515`, part=50.38%), Chicomuselo (CHIAPAS, `cve_geo=07030`, part=47.81%), Olintla (PUEBLA, `cve_geo=21108`, part=63.78%)

### Perfil 4 (553 municipios — 22.33% del total; Lista Nominal 2024: 57,777,865)

**Top 5 variables que definen el perfil (SHAP por cluster):**

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `brecha_generacional_60_vs_18_29` | `1.4216` | `0.1936` | `0.1413` | `+0.70` | ALTA (+) |
| `brecha_genero_tendencia` | `1.2738` | `0.0001` | `0.0046` | `-0.53` | BAJA (-) |
| `part_media_global` | `0.9632` | `0.5008` | `0.5616` | `-0.59` | BAJA (-) |
| `pendiente_tendencia` | `0.7407` | `-0.0001` | `0.0139` | `-0.48` | BAJA (-) |
| `cagr_ln_2009_2024` | `0.7169` | `0.0193` | `0.0135` | `+0.22` | ALTA (+) |

- **Entidades predominantes:** OAXACA (158 muns, 28.57%), VERACRUZ (57 muns, 10.31%), ESTADO DE MEXICO (45 muns, 8.14%), HIDALGO (31 muns, 5.61%), GUANAJUATO (21 muns, 3.8%)
- **Municipios más representativos (cercanos al centroide):** Salamanca (GUANAJUATO, `cve_geo=11027`, part=48.92%), Durango (DURANGO, `cve_geo=10005`, part=47.07%), Coatzintla (VERACRUZ, `cve_geo=30042`, part=50.89%), Fresnillo (ZACATECAS, `cve_geo=32010`, part=53.08%), San Francisco del RincÃ³n (GUANAJUATO, `cve_geo=11031`, part=50.2%)

### Perfil 5 (488 municipios — 19.7% del total; Lista Nominal 2024: 11,612,921)

**Top 5 variables que definen el perfil (SHAP por cluster):**

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `cagr_ln_2009_2024` | `3.2131` | `0.0004` | `0.0135` | `-0.50` | BAJA (-) |
| `brecha_genero_media` | `2.3363` | `0.0460` | `0.0772` | `-0.87` | BAJA (-) |
| `part_media_global` | `0.5071` | `0.4962` | `0.5616` | `-0.64` | BAJA (-) |
| `constancia_sobre_mediana` | `0.4711` | `0.2517` | `0.4991` | `-0.70` | BAJA (-) |
| `volatilidad` | `0.3132` | `0.0933` | `0.1011` | `-0.16` | BAJA (-) |

- **Entidades predominantes:** OAXACA (179 muns, 36.68%), VERACRUZ (61 muns, 12.5%), MICHOACAN (56 muns, 11.48%), CHIHUAHUA (43 muns, 8.81%), DURANGO (27 muns, 5.53%)
- **Municipios más representativos (cercanos al centroide):** Vega de Alatorre (VERACRUZ, `cve_geo=30191`, part=52.76%), TÃ©cpan de Galeana (GUERRERO, `cve_geo=12058`, part=52.8%), Tierra Blanca (VERACRUZ, `cve_geo=30173`, part=50.03%), Guerrero (CHIHUAHUA, `cve_geo=08031`, part=44.86%), Huetamo (MICHOACAN, `cve_geo=16038`, part=46.49%)

---

## 3. Dinámica Temporal por Ventanas Móviles (`2009-2015` $\rightarrow$ `2012-2018` $\rightarrow$ `2015-2021` $\rightarrow$ `2018-2024`)

- **Municipios evaluados:** `2,477`
- **Municipios que cambiaron de perfil entre `2009-2015` y `2018-2024`:** `1,565` (`63.18%`)
- **Municipios que permanecieron en el mismo perfil estructural:** `912`

### Principales Flujos de Transición (`2009-2015` $\rightarrow$ `2018-2024`)

| Perfil Origen (`2009-2015`) | Perfil Destino (`2018-2024`) | Número de Municipios |
| :---: | :---: | ---: |
| Perfil 2 | Perfil 0 | 191 |
| Perfil 4 | Perfil 1 | 158 |
| Perfil 4 | Perfil 0 | 135 |
| Perfil 5 | Perfil 0 | 133 |
| Perfil 2 | Perfil 1 | 131 |
| Perfil 2 | Perfil 4 | 114 |
| Perfil 1 | Perfil 0 | 100 |
| Perfil 0 | Perfil 1 | 95 |
| Perfil 5 | Perfil 4 | 94 |
| Perfil 1 | Perfil 4 | 79 |

### Top 15 Municipios con Mayor Movimiento y Cambio de Perfil (`2009-2015` $\rightarrow$ `2018-2024`)

| `cve_geo` | Municipio | Entidad | Perfil `09-15` | Perfil `18-24` | Part. 2009 | Part. 2024 | Cambio $\Delta$ (p.p.) | Lista Nominal 2024 |
| :---: | :--- | :--- | :---: | :---: | ---: | ---: | ---: | ---: |
| `26006` | Atil | SONORA | Perfil 0 | Perfil 3 | 84.5% | 0.0% | -84.5 p.p. | 747 |
| `19029` | Higueras | NUEVO LEON | Perfil 0 | Perfil 3 | 82.5% | 0.0% | -82.5 p.p. | 1,541 |
| `20048` | Magdalena OcotlÃ¡n | OAXACA | Perfil 2 | Perfil 0 | 0.0% | 82.1% | +82.1 p.p. | 879 |
| `26031` | Oquitoa | SONORA | Perfil 0 | Perfil 3 | 80.1% | 0.0% | -80.1 p.p. | 446 |
| `26016` | Cucurpe | SONORA | Perfil 0 | Perfil 3 | 75.2% | 0.0% | -75.2 p.p. | 1,009 |
| `26043` | Tubutama | SONORA | Perfil 0 | Perfil 3 | 73.8% | 0.0% | -73.8 p.p. | 1,381 |
| `19044` | Rayones | NUEVO LEON | Perfil 2 | Perfil 0 | 0.0% | 65.3% | +65.3 p.p. | 3,040 |
| `26038` | SÃ¡ric | SONORA | Perfil 0 | Perfil 3 | 70.4% | 5.2% | -65.2 p.p. | 1,807 |
| `07055` | Metapa | CHIAPAS | Perfil 2 | Perfil 0 | 0.0% | 64.2% | +64.2 p.p. | 5,217 |
| `07088` | Suchiate | CHIAPAS | Perfil 2 | Perfil 0 | 5.0% | 63.0% | +58.0 p.p. | 25,140 |
| `20510` | Santo Domingo IxcatlÃ¡n | OAXACA | Perfil 2 | Perfil 0 | 0.0% | 58.0% | +58.0 p.p. | 514 |
| `26052` | Pitiquito | SONORA | Perfil 0 | Perfil 3 | 65.2% | 7.8% | -57.5 p.p. | 6,420 |
| `20280` | San Miguel Tenango | OAXACA | Perfil 4 | Perfil 3 | 57.1% | 0.0% | -57.1 p.p. | 637 |
| `29049` | Santa Isabel Xiloxoxtla | TLAXCALA | Perfil 2 | Perfil 1 | 28.1% | 83.8% | +55.7 p.p. | 3,721 |
| `29047` | San Juan Huactzinco | TLAXCALA | Perfil 1 | Perfil 0 | 25.7% | 80.7% | +55.0 p.p. | 5,894 |

---

## 4. Limitaciones Metodológicas y Caveats Éticos

1. **Falacia Ecológica (Principio Inquebrantable #2):** Las asociaciones estadísticas entre participación, estructura etaria, género y ruralidad están medidas a nivel de agregado territorial (`municipio`). Inferir conductas individuales a partir de estos perfiles constituiría una falacia ecológica.
2. **Municipios con Lista Nominal Pequeña (`flag_baja_confiabilidad`):** En municipios con menos de 1,000 electores en lista nominal promedio, variaciones de pocas decenas de votantes (por migración estacional o conflictos locales) producen oscilaciones porcentuales amplias. Estos municipios están debidamente marcados con `flag_baja_confiabilidad = true`.
3. **Cambios de Marco Cartográfico Electoral (2009–2024):** Los municipios creados con posterioridad a 2009 (p. ej. Bacalar, Puerto Morelos, San Quintín, San Felipe, Seybaplaya, Dzitbalché) tienen trayectoria observada únicamente a partir de su primera elección federal tras su creación; los años previos utilizan imputación documentada por mediana estatal (`flag_imputacion_trayectoria = true`) y están identificados en `puente_municipio_anio.parquet`.
4. **Exclusión de Casillas Especiales en Cuadernillos Censales:** Como documenta la DECEyEC del INE, los conteos censales provienen de los cuadernillos de lista nominal de casillas ordinarias/contiguas/extraordinarias, por lo que no incluyen votantes en tránsito en casillas especiales.
