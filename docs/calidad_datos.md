# Reporte de Calidad de Datos e Integridad de Ingesta (CCPC 2009–2024)

## 1. Resumen de Validación y Conciliación de Totales

- **Archivos procesados:** 192 archivos CSV ordinarios (32 entidades × 6 elecciones) + 2 archivos nacionales de modalidades especiales 2024 (`VotoAnticipado2024` y `PrisionPreventiva2024`).
- **Filas crudas totales inspeccionadas (presencial):** 54,872,712
- **Celdas con participación > 100% (`SV > LN`):** 0
- **Celdas con participación < 0% (`SV < 0` o `LN < 0`):** 0
- **Celdas donde `LN != SV + NV + NS`:** 0

## 2. Métricas de Calidad por Año Electoral (Modalidad Presencial)

| Año | Filas Crudas | Nulos en `DEF` | Nulos en `DEL` | Filas con `EDAD > 100` | `LN` en `EDAD > 100` | Filas con `NS > 0` | Total `NS` (No Especificados) | `SV > LN` | `SV < 0` |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2009 | 8,706,843 | 17,351 | 17,351 | 32,761 | 34,028 | 330,583 | 1,865,894 | 0 | 0 |
| 2012 | 8,604,456 | 9,483 | 9,483 | 10,318 | 10,522 | 36,137 | 168,649 | 0 | 0 |
| 2015 | 9,106,059 | 0 | 0 | 12,123 | 12,345 | 894,114 | 5,118,976 | 0 | 0 |
| 2018 | 9,251,122 | 0 | 0 | 10,320 | 10,468 | 1,099,866 | 6,089,742 | 0 | 0 |
| 2021 | 9,430,502 | 0 | 0 | 13,216 | 13,530 | 764,135 | 4,043,320 | 0 | 0 |
| 2024 | 9,773,730 | 0 | 20,912 | 12,891 | 13,197 | 1,123,163 | 6,325,654 | 0 | 0 |

## 3. Hallazgos de Calidad y Reglas Aplicadas

1. **Nulos en `DEL` (Distrito Electoral Local) en 2024:** Se detectaron valores nulos en la columna `DEL` en secciones electorales de 2024. Se normalizaron con el código `'SN'` (Sin Número/No especificado) sin afectar la agregación municipal (`cve_geo`) ni distrital federal (`DEF`).
2. **Edades extremas (`EDAD > 100`):** Existen registros censales de personas con edades reportadas entre 101 y 125 años en el padrón. Al agrupar en el esquema unificado bajo el corte `rango_edad = '60+'`, se evita distorsión por valores extremos individuales sin perder un solo elector de la Lista Nominal.
3. **Registros No Especificados (`NS > 0`):** Corresponden a cuadernillos no disponibles para captura o requeridos por autoridades jurisdiccionales. Se preservan explícitamente en la columna `no_especificados`.
4. **Regla de Privacidad (`< 10`):** Toda celda en el esquema unificado con `lista_nominal < 10` (o `< 10` votantes en modalidades sin LN) lleva la bandera `celda_pequena_lt10 = true`, y en las vistas analíticas (`v_municipio_eleccion`, `v_distrito_eleccion`) las tasas de subgrupos con denominador `< 10` se suprimen (`NULL`).

## 4. Tabla Puente Municipio-Año (`puente_municipio_anio`)

- **Total de claves municipales únicas (`cve_geo`) 2009–2024:** 2,477
- **Municipios con panel completo (6 de 6 elecciones):** 2,455
- **Municipios con cambio en el marco geográfico (nueva creación o fusión):** 22

### Desglose por Estatus del Marco Geográfico

| Estatus | Número de Municipios |
| :--- | ---: |
| `ESTABLE_2009_2024` | 2,455 |
| `NUEVA_CREACION_2024` | 9 |
| `NUEVA_CREACION_2021` | 5 |
| `NUEVA_CREACION_2018` | 5 |
| `INTERMITENTE_O_CASO_ESPECIAL` | 3 |

### Detalle de Municipios con Cambios de Marco Geográfico (2009–2024)

| `cve_geo` | Entidad | Municipio | Primer Año | Último Año | Elecciones Presente | Estatus |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| `07117` | CHIAPAS | San AndrÃ©s Duraznal | 2009 | 2024 | 5 | `INTERMITENTE_O_CASO_ESPECIAL` |
| `20144` | OAXACA | San Francisco NuxaÃ±o | 2009 | 2024 | 5 | `INTERMITENTE_O_CASO_ESPECIAL` |
| `20218` | OAXACA | San Juan Teita | 2009 | 2024 | 5 | `INTERMITENTE_O_CASO_ESPECIAL` |
| `07120` | CHIAPAS | RincÃ³n Chamula San Pedro | 2018 | 2024 | 3 | `NUEVA_CREACION_2018` |
| `07121` | CHIAPAS | El Parral | 2018 | 2024 | 3 | `NUEVA_CREACION_2018` |
| `07122` | CHIAPAS | Emiliano Zapata | 2018 | 2024 | 3 | `NUEVA_CREACION_2018` |
| `07123` | CHIAPAS | Mezcalapa | 2018 | 2024 | 3 | `NUEVA_CREACION_2018` |
| `07124` | CHIAPAS | Honduras de la Sierra | 2018 | 2024 | 3 | `NUEVA_CREACION_2018` |
| `04012` | CAMPECHE | DzitbalchÃ© | 2021 | 2024 | 2 | `NUEVA_CREACION_2021` |
| `04013` | CAMPECHE | Seybaplaya | 2021 | 2024 | 2 | `NUEVA_CREACION_2021` |
| `07119` | CHIAPAS | CapitÃ¡n Luis Ãngel Vidal | 2021 | 2024 | 2 | `NUEVA_CREACION_2021` |
| `17034` | MORELOS | Coatetelco | 2021 | 2024 | 2 | `NUEVA_CREACION_2021` |
| `17035` | MORELOS | Xoxocotla | 2021 | 2024 | 2 | `NUEVA_CREACION_2021` |
| `02006` | BAJA CALIFORNIA | San Quintin | 2024 | 2024 | 1 | `NUEVA_CREACION_2024` |
| `02007` | BAJA CALIFORNIA | San Felipe | 2024 | 2024 | 1 | `NUEVA_CREACION_2024` |
| `12082` | GUERRERO | Ãuu Savi | 2024 | 2024 | 1 | `NUEVA_CREACION_2024` |
| `12083` | GUERRERO | Las Vigas | 2024 | 2024 | 1 | `NUEVA_CREACION_2024` |
| `12084` | GUERRERO | San NicolÃ¡s | 2024 | 2024 | 1 | `NUEVA_CREACION_2024` |
| `12085` | GUERRERO | Santa Cruz del RincÃ³n | 2024 | 2024 | 1 | `NUEVA_CREACION_2024` |
| `17036` | MORELOS | Hueyapan | 2024 | 2024 | 1 | `NUEVA_CREACION_2024` |
| `25019` | SINALOA | Eldorado | 2024 | 2024 | 1 | `NUEVA_CREACION_2024` |
| `25020` | SINALOA | Juan JosÃ© RÃ­os | 2024 | 2024 | 1 | `NUEVA_CREACION_2024` |
