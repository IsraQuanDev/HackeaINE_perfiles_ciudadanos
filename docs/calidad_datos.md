# Reporte de Calidad de Datos e Integridad de Ingesta Medallion (CCPC 2009–2024 · v2)

## 1. Resumen de Validación y Conciliación de Totales

- **Archivos procesados:** 192 archivos CSV ordinarios (32 entidades × 6 elecciones) + 2 archivos nacionales de modalidades especiales 2024 (`VotoAnticipado2024` y `PrisionPreventiva2024`).
- **Filas crudas totales inspeccionadas (presencial):** 54,872,712
- **Celdas con participación > 100% (`SV > LN`):** 0
- **Celdas con participación < 0% (`SV < 0` o `LN < 0`):** 0
- **Celdas donde `LN != SV + NV + NS`:** 0
- **Celdas municipio-año con `cobertura < 90%` convertidas a `NA` (nunca `0%`):** 1889
- **Normalización Unicode:** `UTF-8 NFC` verificado en los 2,477 municipios y 32 entidades (`0` ocurrencias de mojibake `Ã` o `Â`).

## 2. Métricas de Calidad por Año Electoral (Modalidad Presencial)

| Año | Filas Crudas | Nulos en `DEF` | Nulos en `DEL` | Filas con `EDAD > 100` | `LN` en `EDAD > 100` | Filas con `NS > 0` | Total `NS` (No Especificados) | `SV > LN` | `SV < 0` |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2009 | 8,706,843 | 17,351 | 17,351 | 32,761 | 34,028 | 330,583 | 1,865,894 | 0 | 0 |
| 2012 | 8,604,456 | 9,483 | 9,483 | 10,318 | 10,522 | 36,137 | 168,649 | 0 | 0 |
| 2015 | 9,106,059 | 0 | 0 | 12,123 | 12,345 | 894,114 | 5,118,976 | 0 | 0 |
| 2018 | 9,251,122 | 0 | 0 | 10,320 | 10,468 | 1,099,866 | 6,089,742 | 0 | 0 |
| 2021 | 9,430,502 | 0 | 0 | 13,216 | 13,530 | 764,135 | 4,043,320 | 0 | 0 |
| 2024 | 9,773,730 | 0 | 20,912 | 12,891 | 13,197 | 1,123,163 | 6,325,654 | 0 | 0 |

## 3. Reglas Contractuales Silver/Gold (Plan v2)

1. **Definición Oficial de Participación y Cobertura:** $\text{participacion} = SV / (SV + NV)$ excluyendo `NS` del denominador; $\text{cobertura} = (SV + NV) / LN$. Si $\text{cobertura} < 0.90$, la participación se marca como `NULL` (`NA`) y `flag_calidad = 'BAJA_COBERTURA_NS'`.
2. **Codificación UTF-8 NFC por Archivo:** Los archivos 2009–2024 se inspeccionan individualmente con `detect_file_encoding()` y se reparan con `fix_mojibake_utf8_nfc()`.
3. **Curvas Etarias (8 Grupos) y Cohortes:** Se preservan los 8 tramos (`18-19`, `20-24`, `25-29`, `30-39`, `40-49`, `50-59`, `60-69`, `70+`) y las pseudo-cohortes de primer voto (`18-20` y `21-23`).
4. **Privacidad (`< 10` y `SEXO = 2`):** Celdas con denominador `< 10` se suprimen en tasas agregadas (`NULL`).

## 4. Tabla Puente Municipio-Año (`puente_municipio_anio`)

- **Total de claves municipales únicas (`cve_geo`) 2009–2024:** 2,477
- **Municipios con panel completo (6 de 6 elecciones):** 2,455
- **Municipios de nueva creación post-2009:** 22

| Estatus | Número de Municipios |
| :--- | ---: |
| `ESTABLE_2009_2024` | 2,455 |
| `NUEVA_CREACION_2024` | 9 |
| `NUEVA_CREACION_2021` | 5 |
| `NUEVA_CREACION_2018` | 5 |
| `INTERMITENTE_O_CASO_ESPECIAL` | 3 |
