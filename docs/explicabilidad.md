# Explicabilidad de Perfiles, Medoides Reales y Dinámica Markoviana (`docs/explicabilidad.md` · v2)

## 1. Modelos Sustitutos de Explicabilidad Global (Árbol de Decisión + LightGBM SHAP)

- **Exactitud del Árbol de Decisión interpretable (`max_depth=3`):** `68.55%`
- **Exactitud del modelo LightGBM sustituto + TreeExplainer SHAP:** `100.00%`

### Ranking Global de Importancia SHAP (`mean(|SHAP|)`)

| Orden | Variable | Importancia Media Absoluta SHAP |
| :---: | :--- | ---: |
| 1 | `brecha_juvenil_18_29_vs_30_59` | `0.82733` |
| 2 | `volatilidad` | `0.78793` |
| 3 | `retencion_primer_voto` | `0.70308` |
| 4 | `part_media_global` | `0.61856` |
| 5 | `rezago_espacial_part` | `0.53039` |
| 6 | `pendiente_tendencia` | `0.49873` |
| 7 | `caida_presidencial_intermedia` | `0.49612` |
| 8 | `constancia_sobre_mediana` | `0.37963` |
| 9 | `brecha_genero_media` | `0.37568` |
| 10 | `pct_ln_rural` | `0.28787` |

### Reglas del Árbol de Decisión de Poca Profundidad (`max_depth=3`)

```text
|--- volatilidad <= 0.06
|   |--- brecha_juvenil_18_29_vs_30_59 <= -0.13
|   |   |--- part_media_global <= 0.57
|   |   |   |--- class: 2
|   |   |--- part_media_global >  0.57
|   |   |   |--- class: 2
|   |--- brecha_juvenil_18_29_vs_30_59 >  -0.13
|   |   |--- rezago_espacial_part <= 0.55
|   |   |   |--- class: 4
|   |   |--- rezago_espacial_part >  0.55
|   |   |   |--- class: 1
|--- volatilidad >  0.06
|   |--- volatilidad <= 0.12
|   |   |--- part_media_global <= 0.57
|   |   |   |--- class: 4
|   |   |--- part_media_global >  0.57
|   |   |   |--- class: 2
|   |--- volatilidad >  0.12
|   |   |--- rezago_espacial_part <= 0.68
|   |   |   |--- class: 3
|   |   |--- rezago_espacial_part >  0.68
|   |   |   |--- class: 0
```

---

## 2. Variables Definitorias (SHAP), Curvas de Edad y Municipio Prototipo Real (Medoide)

### Perfil 0 (111 municipios — 4.48% del total; Lista Nominal 2024: 1,718,428)

- **Municipio Prototipo Real (Medoide más cercano al centro del perfil):** **Baca, Yucatán** (`cve_geo = 31004`, participación media `81.14%`, distancia al centroide `0.4099`).

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `rezago_espacial_part` | `9.1161` | `0.7811` | `0.5845` | `+2.75` | ALTA (+) |
| `part_media_global` | `4.3739` | `0.7926` | `0.5837` | `+2.11` | ALTA (+) |
| `volatilidad` | `1.2356` | `0.1019` | `0.0873` | `+0.37` | ALTA (+) |
| `retencion_primer_voto` | `1.1254` | `0.9843` | `0.8877` | `+0.93` | ALTA (+) |
| `brecha_juvenil_18_29_vs_30_59` | `0.4464` | `-0.0639` | `-0.1167` | `+0.95` | ALTA (+) |

### Perfil 1 (537 municipios — 21.68% del total; Lista Nominal 2024: 23,639,337)

- **Municipio Prototipo Real (Medoide más cercano al centro del perfil):** **Mazamitla, Jalisco** (`cve_geo = 14061`, participación media `66.07%`, distancia al centroide `0.6913`).

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `volatilidad` | `3.4724` | `0.0432` | `0.0873` | `-1.12` | BAJA (-) |
| `rezago_espacial_part` | `1.4024` | `0.6342` | `0.5845` | `+0.70` | ALTA (+) |
| `brecha_juvenil_18_29_vs_30_59` | `1.3821` | `-0.0757` | `-0.1167` | `+0.74` | ALTA (+) |
| `caida_presidencial_intermedia` | `1.2785` | `0.0452` | `0.1157` | `-0.99` | BAJA (-) |
| `part_media_global` | `0.5879` | `0.6508` | `0.5837` | `+0.68` | ALTA (+) |

### Perfil 2 (425 municipios — 17.16% del total; Lista Nominal 2024: 9,287,589)

- **Municipio Prototipo Real (Medoide más cercano al centro del perfil):** **Altotonga, Veracruz** (`cve_geo = 30011`, participación media `59.9%`, distancia al centroide `0.64`).

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `brecha_juvenil_18_29_vs_30_59` | `2.5298` | `-0.1659` | `-0.1167` | `-0.89` | BAJA (-) |
| `pct_ln_rural` | `1.5223` | `0.5789` | `0.3345` | `+0.87` | ALTA (+) |
| `brecha_genero_media` | `0.9573` | `0.1000` | `0.0798` | `+0.54` | ALTA (+) |
| `part_media_global` | `0.7347` | `0.6178` | `0.5837` | `+0.35` | ALTA (+) |
| `caida_presidencial_intermedia` | `0.5960` | `0.0822` | `0.1157` | `-0.47` | BAJA (-) |

### Perfil 3 (554 municipios — 22.37% del total; Lista Nominal 2024: 18,074,124)

- **Municipio Prototipo Real (Medoide más cercano al centro del perfil):** **Oriental, Puebla** (`cve_geo = 21109`, participación media `59.82%`, distancia al centroide `0.4548`).

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `pendiente_tendencia` | `3.0632` | `0.0597` | `0.0228` | `+1.07` | ALTA (+) |
| `volatilidad` | `2.6039` | `0.1353` | `0.0873` | `+1.22` | ALTA (+) |
| `caida_presidencial_intermedia` | `1.4522` | `0.1829` | `0.1157` | `+0.95` | ALTA (+) |
| `retencion_primer_voto` | `0.6813` | `0.9151` | `0.8877` | `+0.26` | ALTA (+) |
| `part_media_global` | `0.2585` | `0.5803` | `0.5837` | `-0.03` | BAJA (-) |

### Perfil 4 (659 municipios — 26.6% del total; Lista Nominal 2024: 45,053,420)

- **Municipio Prototipo Real (Medoide más cercano al centro del perfil):** **La Antigua, Veracruz** (`cve_geo = 30017`, participación media `52.7%`, distancia al centroide `0.6366`).

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `retencion_primer_voto` | `1.7775` | `0.8203` | `0.8877` | `-0.65` | BAJA (-) |
| `constancia_sobre_mediana` | `1.3701` | `0.1345` | `0.4865` | `-0.94` | BAJA (-) |
| `part_media_global` | `1.3523` | `0.4997` | `0.5837` | `-0.85` | BAJA (-) |
| `brecha_genero_media` | `0.5540` | `0.0672` | `0.0798` | `-0.34` | BAJA (-) |
| `brecha_juvenil_18_29_vs_30_59` | `0.4303` | `-0.1157` | `-0.1167` | `+0.02` | ALTA (+) |

### Perfil 5 (191 municipios — 7.71% del total; Lista Nominal 2024: 557,450)

- **Municipio Prototipo Real (Medoide más cercano al centro del perfil):** **San Pedro Molinos, Oaxaca** (`cve_geo = 20318`, participación media `52.38%`, distancia al centroide `0.7335`).

| Variable | `mean(|SHAP|)` | Media del Perfil | Media Nacional | Z-Score vs. País | Dirección |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `retencion_primer_voto` | `4.7117` | `1.0469` | `0.8877` | `+1.53` | ALTA (+) |
| `brecha_juvenil_18_29_vs_30_59` | `3.0713` | `-0.1909` | `-0.1167` | `-1.34` | BAJA (-) |
| `brecha_genero_media` | `1.4385` | `0.0467` | `0.0798` | `-0.88` | BAJA (-) |
| `constancia_sobre_mediana` | `0.7688` | `0.1266` | `0.4865` | `-0.96` | BAJA (-) |
| `rezago_espacial_part` | `0.6718` | `0.5209` | `0.5845` | `-0.89` | BAJA (-) |

---

## 3. Dinámica Temporal por Ventanas Móviles y Cadena de Markov

- **Municipios evaluados:** `2,477`
- **Permanencia media en la diagonal de Markov:** `72.5%` vs. `16.7%` bajo azar uniforme (**`4.35x` más estable que el azar**).
- **Municipios que cambiaron de perfil entre `2009-2015` y `2018-2024`:** `1,219` (`49.21%`).

### Top 15 Municipios con Cambio Real de Perfil (Excluyendo Celdas con Baja Cobertura `NS`)

| `cve_geo` | Municipio | Entidad | Perfil `09-15` | Perfil `18-24` | Part. 2009 (Real) | Part. 2024 (Real) | Cambio $\Delta$ (p.p.) | Lista Nominal 2024 |
| :---: | :--- | :--- | :---: | :---: | ---: | ---: | ---: | ---: |
| `29047` | San Juan Huactzinco | Tlaxcala | Perfil 4 | Perfil 3 | 25.7% | 80.7% | +55.0 p.p. | 5,894 |
| `21069` | Hermenegildo Galeana | Puebla | Perfil 3 | Perfil 1 | 20.8% | 75.2% | +54.4 p.p. | 5,544 |
| `21013` | Altepexi | Puebla | Perfil 3 | Perfil 1 | 24.1% | 77.6% | +53.5 p.p. | 15,121 |
| `21006` | Ahuacatlán | Puebla | Perfil 3 | Perfil 1 | 30.5% | 80.9% | +50.4 p.p. | 11,390 |
| `21005` | Acteopan | Puebla | Perfil 3 | Perfil 1 | 35.6% | 83.7% | +48.0 p.p. | 2,319 |
| `08049` | Nonoava | Chihuahua | Perfil 4 | Perfil 1 | 28.5% | 75.4% | +46.9 p.p. | 2,918 |
| `21147` | Santa Inés Ahuatempan | Puebla | Perfil 3 | Perfil 1 | 29.2% | 75.4% | +46.2 p.p. | 4,876 |
| `29056` | San Jerónimo Zacualpan | Tlaxcala | Perfil 3 | Perfil 1 | 39.7% | 84.2% | +44.5 p.p. | 3,276 |
| `21107` | Ocoyucan | Puebla | Perfil 4 | Perfil 1 | 20.8% | 64.8% | +44.1 p.p. | 33,389 |
| `29039` | Xaloztoc | Tlaxcala | Perfil 3 | Perfil 1 | 27.8% | 71.8% | +43.9 p.p. | 18,969 |
| `21181` | Tlaltenango | Puebla | Perfil 4 | Perfil 1 | 29.1% | 72.5% | +43.3 p.p. | 5,406 |
| `29028` | Teolocholco | Tlaxcala | Perfil 3 | Perfil 1 | 33.0% | 76.1% | +43.2 p.p. | 19,434 |
| `21139` | San Nicolás de los Ranchos | Puebla | Perfil 5 | Perfil 1 | 31.0% | 73.8% | +42.8 p.p. | 8,672 |
| `21100` | Molcaxac | Puebla | Perfil 3 | Perfil 1 | 31.9% | 74.2% | +42.3 p.p. | 5,147 |
| `29052` | La Magdalena Tlaltelulco | Tlaxcala | Perfil 3 | Perfil 1 | 36.0% | 78.2% | +42.3 p.p. | 15,172 |
