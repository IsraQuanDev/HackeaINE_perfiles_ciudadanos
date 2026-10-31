# Documentación de Fuentes de Datos y Enriquecimiento Externo

## 1. Fuente Primaria: Plataforma de Conteos Censales de Participación Ciudadana (CCPC) — INE
- **Institución:** Instituto Nacional Electoral (INE) — Dirección Ejecutiva de Capacitación Electoral y Educación Cívica (DECEyEC).
- **Cobertura temporal:** Procesos Electorales Federales 2008-2009, 2011-2012, 2014-2015, 2017-2018, 2020-2021 y 2023-2024.
- **Modalidades incluidas:**
  1. **Votación Presencial en Casillas Ordinarias (2009–2024):** 192 archivos CSV estatales (32 entidades × 6 elecciones), desglosados por sección electoral (`SECCION`), tipo de sección (`TIPOSEC`: Urbana, Mixta, Rural), distrito federal (`DEF`), distrito local (`DEL`), sexo (`SEXO`: 0 Hombres, 1 Mujeres, 2 No binario en 2024) y edad cumplida (`EDAD`: 18 a 125 años).
  2. **Voto Anticipado (2024):** 1 archivo CSV nacional desglosado por entidad, municipio, distrito federal/local y sexo.
  3. **Voto de Personas en Prisión Preventiva (2024):** 1 archivo CSV nacional desglosado por entidad, distrito federal y sexo (sin clave municipal).
- **Variables sociodemográficas obtenidas directamente del CCPC (sin necesidad de imputación externa):**
  - Estructura etaria del padrón/lista nominal por municipio: `% 18-29 años` y `% 60+ años`.
  - Tasas de participación específicas por grupo etario (`18-29`, `30-59`, `60+`) y brecha generacional.
  - Tasas de participación específicas por sexo (`Mujeres` vs. `Hombres`) y brecha de género.
  - Grado de urbanización electoral municipal: `% de Lista Nominal en secciones Urbanas (U), Mixtas (M) y Rurales (R)`.

---

## 2. Fuentes de Enriquecimiento Externo (Nivel Municipal)

### 2.1 CONAPO — Índice de Marginación por Municipio 2020
- **Institución:** Consejo Nacional de Población (CONAPO), con base en el Censo de Población y Vivienda 2020 (INEGI).
- **Versión:** `IMM_2020` (Publicación oficial 2021, Marco Geoestadístico 2020).
- **URL oficial de descarga:** `http://www.conapo.gob.mx/work/models/CONAPO/Marginacion/Datos_Abiertos/Municipio/IMM_2020.csv`
- **Campos utilizados:**
  - `CVE_MUN` $\rightarrow$ normalizado a `cve_geo` (5 dígitos).
  - `IM_2020` $\rightarrow$ `conapo_indice_marginacion_2020` (Índice de marginación municipal).
  - `GM_2020` $\rightarrow$ `conapo_grado_marginacion_2020` (Muy bajo, Bajo, Medio, Alto, Muy alto).
  - `ANALF` $\rightarrow$ `conapo_pct_analfabetismo_2020` (% de población de 15 años o más analfabeta).
  - `SBASC` $\rightarrow$ `conapo_pct_sin_educ_basica_2020` (% de población de 15 años o más sin educación básica).

### 2.2 INEGI — Censo de Población y Vivienda 2020 (Principales Resultados por Localidad / Municipio ITER)
- **Institución:** Instituto Nacional de Estadística y Geografía (INEGI).
- **Versión:** Censo 2020 (`ITER_NALCSV20.zip` — Nivel Municipal, `LOC == 0000`).
- **URL oficial de descarga:** `https://www.inegi.org.mx/contenidos/programas/ccpv/2020/microdatos/iter/ITER_NALCSV20.zip`
- **Campos del esquema esperado:**
  - `GRAPROES` $\rightarrow$ `inegi_grado_escolaridad_2020` (Grado promedio de escolaridad).
  - `VPH_INTER` / `TVIVPARHAB` $\rightarrow$ `inegi_pct_viviendas_internet_2020` (% de viviendas particulares habitadas que disponen de internet).

---

## 3. Instrucciones de Descarga Reproducible y Regla de Honestidad Metodológica

El módulo [`src/features/enrichment.py`](file:///c:/Users/52477/Desktop/hackaton2INE/src/features/enrichment.py) ejecuta automáticamente la descarga de `IMM_2020.csv` hacia `data/raw/external/`.

Para colocar manualmente el archivo consolidado en entornos sin salida a internet:
1. Descargue `IMM_2020.csv` de CONAPO y/o el `ITER_NALCSV20.zip` de INEGI.
2. Guarde el archivo en `data/raw/external/enriquecimiento_inegi_conapo_2020.csv` con las columnas:
   `cve_geo,conapo_indice_marginacion_2020,conapo_grado_marginacion_2020,conapo_pct_analfabetismo_2020,conapo_pct_sin_educ_basica_2020,inegi_grado_escolaridad_2020,inegi_pct_viviendas_internet_2020`.
3. Si el entorno tiene red restringida y el archivo no está presente, el pipeline activa `flag_enriquecimiento_externo_stub = True` y deja `NaN` en los campos no disponibles, **cumpliendo estrictamente la prohibición de inventar datos** (Principio Inquebrantable #3).
