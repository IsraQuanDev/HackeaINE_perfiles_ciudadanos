# Inventario de Datos: Conteos Censales de Participación Ciudadana (CCPC 2009–2024)

## 1. Resumen Verificado de Directorios y Archivos Fuente

| Directorio | Elección / Modalidad | Archivos CSV | Tamaño Total | Codificación / BOM | Granularidad Real |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `DatosAbiertos_DECEyEC_ConteosCensales2009` | Intermedia Federal (2009) | 32 | 587.03 MB | Latin-1 (`cp1252`), sin BOM | `SECCION` × `SEXO` × `EDAD` |
| `DatosAbiertos_DECEyEC_ConteosCensales2012` | Presidencial Federal (2012) | 32 | 580.11 MB | Latin-1 (`cp1252`), sin BOM | `SECCION` × `SEXO` × `EDAD` |
| `DatosAbiertos_DECEyEC_ConteosCensales2015` | Intermedia Federal (2015) | 32 | 613.22 MB | Latin-1 (`cp1252`), sin BOM | `SECCION` × `SEXO` × `EDAD` |
| `DatosAbiertos_DECEyEC_ConteosCensales2018` | Presidencial Federal (2018) | 32 | 623.27 MB | Latin-1 (`cp1252`), sin BOM | `SECCION` × `SEXO` × `EDAD` |
| `DatosAbiertos_DECEyEC_ConteosCensales2021` | Intermedia Federal (2021) | 32 | 635.48 MB | Latin-1 (`cp1252`), sin BOM | `SECCION` × `SEXO` × `EDAD` |
| `DatosAbiertos_DECEyEC_ConteosCensales2024` | Presidencial Federal (2024) | 32 | 688.04 MB | Prefijo BOM (`\ufeffAELEC`) + Latin-1 | `SECCION` × `SEXO` × `EDAD` |
| `..._VotoAnticipado2024` | Voto Anticipado (2024) | 1 | 0.15 MB | Prefijo BOM (`\ufeffAELEC`) + Latin-1 | Registro individual por `MPIOCVE` × `DEF` × `DEL` × `SEXO` |
| `..._PrisionPreventiva2024` | Prisión Preventiva (2024) | 1 | 0.60 MB | Prefijo BOM (`\ufeffAELEC`) + Latin-1 | Registro individual por `ESTADO` × `DEF` × `SEXO` (sin municipio) |

## 2. Hallazgos Clave
1. Los 192 archivos ordinarios (2009–2024) contienen desglose por `EDAD` (18 a 125 años), `SEXO` (0 Hombres, 1 Mujeres, 2 No binario en 2024) y `TIPOSEC` (Urbana, Mixta, Rural) a nivel sección electoral.
2. Ningún archivo del CCPC contiene escolaridad ni acceso a internet; dichas variables se documentan e integran mediante el módulo de enriquecimiento externo (`CONAPO` / `INEGI Censo 2020`).
3. El archivo de Prisión Preventiva 2024 no contiene columna de municipio (`MPIOCVE`), por lo que se asigna a `cve_mun = '000'` para preservar los totales distritales (`DEF`) y estatales (`EDOCVE`) sin inventar imputaciones municipales.
