from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DUCKDB_PATH = BASE_DIR / "data" / "ccpc.duckdb"
BRIDGE_PATH = BASE_DIR / "data" / "processed" / "puente_municipio_anio.parquet"
QUALITY_DOC = BASE_DIR / "docs" / "calidad_datos.md"
AUDIT_CEROS_DOC = BASE_DIR / "docs" / "auditoria_ceros.md"


def test_ingest_artifacts_exist() -> None:
    """Verifica que los artefactos Medallion (Bronze, Silver, Gold, Serving) y reportes existan."""
    assert DUCKDB_PATH.exists(), "No existe el catálogo data/ccpc.duckdb"
    assert BRIDGE_PATH.exists(), "No existe la tabla puente_municipio_anio.parquet"
    assert QUALITY_DOC.exists(), "No existe el reporte docs/calidad_datos.md"
    assert AUDIT_CEROS_DOC.exists(), "No existe el reporte docs/auditoria_ceros.md"
    assert (BASE_DIR / "data" / "bronze" / "metadata_ingesta_archivos.parquet").exists()
    assert (BASE_DIR / "data" / "gold" / "v_municipio_eleccion.parquet").exists()
    assert (BASE_DIR / "data" / "serving" / "v_entidad_eleccion.parquet").exists()
    for year in [2009, 2012, 2015, 2018, 2021, 2024]:
        p_int = BASE_DIR / "data" / "interim" / "ccpc_unificado" / f"anio={year}" / "data.parquet"
        p_sil = BASE_DIR / "data" / "silver" / "ccpc_silver" / f"anio={year}" / "data.parquet"
        assert p_int.exists(), f"Falta partición Interim Parquet para el año {year}"
        assert p_sil.exists(), f"Falta partición Silver Parquet para el año {year}"


def test_no_mojibake_and_explicit_utf8_names() -> None:
    """
    Fase A1.1: Falla si algún nombre de entidad o municipio contiene 'Ã' o 'Â'
    y verifica explícitamente: Querétaro, León, Gómez Farías, Rincón de Romos,
    Magdalena Ocotlán, Jesús María, San Luis Potosí.
    """
    bridge = pd.read_parquet(BRIDGE_PATH)
    bad_mun = bridge[bridge["nom_mun"].str.contains("Ã|Â", regex=True, na=False)]
    bad_ent = bridge[bridge["nom_ent"].str.contains("Ã|Â", regex=True, na=False)]
    assert len(bad_mun) == 0, f"Nombres de municipio con mojibake detectados:\n{bad_mun[['cve_geo', 'nom_mun']]}"
    assert len(bad_ent) == 0, f"Nombres de entidad con mojibake detectados:\n{bad_ent[['cve_ent', 'nom_ent']]}"

    all_muns = set(bridge["nom_mun"].unique())
    all_ents = set(bridge["nom_ent"].unique())

    for required_ent in ["Querétaro", "Nuevo León", "San Luis Potosí", "Michoacán", "Yucatán", "Ciudad de México"]:
        assert required_ent in all_ents, f"No se encontró la entidad en UTF-8 limpio: {required_ent}"

    for required_mun in [
        "Querétaro",
        "León",
        "Gómez Farías",
        "Rincón de Romos",
        "Magdalena Ocotlán",
        "Jesús María",
        "San Luis Potosí",
    ]:
        assert required_mun in all_muns, f"No se encontró el municipio en UTF-8 limpio: {required_mun}"


def test_no_spurious_zero_participation_and_coverage_rule() -> None:
    """
    Fase A1.2 & A1.3: Verifica que participacion = SV/(SV+NV) y si cobertura < 0.90 -> NULL (nunca 0%).
    Verifica específicamente Atil, Higueras, Oquitoa, Cucurpe, Tubutama (2024) y Magdalena Ocotlán, Rayones (2009).
    """
    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    spurious_zeros = con.execute("""
        SELECT anio, cve_geo, nom_ent, nom_mun, lista_nominal, votantes, no_votantes, no_especificados, cobertura, participacion
        FROM v_municipio_eleccion
        WHERE participacion = 0.0
    """).df()

    low_cov_not_null = con.execute("""
        SELECT COUNT(*)
        FROM v_municipio_eleccion
        WHERE cobertura < 0.90 AND participacion IS NOT NULL
    """).fetchone()[0]

    specific_cases = con.execute("""
        SELECT anio, cve_geo, nom_mun, cobertura, participacion, flag_calidad
        FROM v_municipio_eleccion
        WHERE (anio = 2024 AND cve_geo IN ('26006', '19029', '26031', '26016', '26043'))
           OR (anio = 2009 AND cve_geo IN ('20048', '19044'))
    """).df()
    con.close()

    assert len(spurious_zeros) == 0, f"Aún existen celdas con participación 0.0% espuria:\n{spurious_zeros}"
    assert low_cov_not_null == 0, f"Existen {low_cov_not_null} celdas con cobertura < 0.90 cuya participación no es NULL"
    assert len(specific_cases) == 7, f"Se esperaban los 7 casos P0-4 documentados, encontrados: {len(specific_cases)}"
    assert specific_cases["participacion"].isna().all(), "Los 7 casos de NS==LN deben tener participacion = NULL (NA)"
    assert (specific_cases["flag_calidad"] == "BAJA_COBERTURA_NS").all()


def test_entity_voter_sums_match_source_exactly() -> None:
    """Verifica que la suma de SV, NV, NS y LN por entidad coincida al 100% con el archivo fuente."""
    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    mismatches = con.execute("""
        SELECT
            c.anio,
            c.modalidad,
            c.cve_ent,
            c.sv_fuente,
            v.votantes AS sv_vista,
            c.ln_fuente,
            v.lista_nominal AS ln_vista
        FROM (
            SELECT anio, modalidad, cve_ent, SUM(sv_fuente) AS sv_fuente, SUM(ln_fuente) AS ln_fuente
            FROM control_totales_fuente
            GROUP BY anio, modalidad, cve_ent
        ) c
        JOIN v_entidad_eleccion v
          ON c.anio = v.anio AND c.modalidad = v.modalidad AND c.cve_ent = v.cve_ent
        WHERE c.sv_fuente != v.votantes OR c.ln_fuente != v.lista_nominal
    """).df()
    con.close()
    assert len(mismatches) == 0, f"Diferencias encontradas entre fuente y vista:\n{mismatches}"


def test_direct_csv_spot_check_against_duckdb() -> None:
    """Verifica directamente contra archivos CSV crudos de distintos años que la suma coincide."""
    raw_ags_2009 = BASE_DIR / "DatosAbiertos_DECEyEC_ConteosCensales2009" / "datosabiertos_deceyec_conteoscensales2009_ags.csv"
    raw_ags_2024 = BASE_DIR / "DatosAbiertos_DECEyEC_ConteosCensales2024" / "datosabiertos_deceyec_conteoscensales2024_ags.csv"

    df_09 = pd.read_csv(raw_ags_2009, encoding="utf-8", low_memory=False)
    df_24 = pd.read_csv(raw_ags_2024, encoding="utf-8-sig", low_memory=False)

    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    res_09 = con.execute(
        "SELECT lista_nominal, votantes FROM v_entidad_eleccion WHERE anio=2009 AND cve_ent='01' AND modalidad='presencial'"
    ).fetchone()
    res_24 = con.execute(
        "SELECT lista_nominal, votantes FROM v_entidad_eleccion WHERE anio=2024 AND cve_ent='01' AND modalidad='presencial'"
    ).fetchone()
    con.close()

    assert res_09 is not None and res_24 is not None
    assert int(df_09["LN"].sum()) == int(res_09[0])
    assert int(df_09["SV"].sum()) == int(res_09[1])
    assert int(df_24["LN"].sum()) == int(res_24[0])
    assert int(df_24["SV"].sum()) == int(res_24[1])


def test_unique_keys_and_no_nulls_in_geo_keys() -> None:
    """Verifica que no existan nulos en cve_ent/cve_mun/anio y que (cve_geo, anio) sea único en v_municipio_eleccion."""
    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    null_counts = con.execute("""
        SELECT
            SUM(CASE WHEN cve_ent IS NULL OR LENGTH(cve_ent) != 2 THEN 1 ELSE 0 END) AS bad_ent,
            SUM(CASE WHEN cve_mun IS NULL OR LENGTH(cve_mun) != 3 THEN 1 ELSE 0 END) AS bad_mun,
            SUM(CASE WHEN cve_geo IS NULL OR LENGTH(cve_geo) != 5 THEN 1 ELSE 0 END) AS bad_geo,
            SUM(CASE WHEN anio IS NULL THEN 1 ELSE 0 END) AS bad_anio
        FROM ccpc_unificado
    """).fetchone()

    dup_mun_year = con.execute("""
        SELECT cve_geo, anio, COUNT(*) AS n
        FROM v_municipio_eleccion
        GROUP BY cve_geo, anio
        HAVING COUNT(*) > 1
    """).df()
    con.close()

    assert null_counts == (0, 0, 0, 0), f"Claves inválidas o nulas detectadas: {null_counts}"
    assert len(dup_mun_year) == 0, f"Claves duplicadas en v_municipio_eleccion:\n{dup_mun_year}"


def test_participation_bounds_and_bridge_integrity() -> None:
    """Verifica que la participación válida esté estrictamente en (0, 1] y que la vista de 8 grupos de edad funcione."""
    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    out_of_bounds = con.execute("""
        SELECT COUNT(*)
        FROM v_municipio_eleccion
        WHERE participacion IS NOT NULL AND (participacion <= 0.0 OR participacion > 1.0)
    """).fetchone()[0]

    age_groups = con.execute("""
        SELECT DISTINCT grupo_edad FROM v_municipio_edad_8grupos ORDER BY grupo_edad
    """).df()["grupo_edad"].tolist()
    con.close()

    assert out_of_bounds == 0, f"Existen {out_of_bounds} registros municipales con participación fuera de (0, 1]"
    assert age_groups == ["18-19", "20-24", "25-29", "30-39", "40-49", "50-59", "60-69", "70+"]

    bridge = pd.read_parquet(BRIDGE_PATH)
    assert bridge["cve_geo"].is_unique, "cve_geo debe ser único en puente_municipio_anio"
    assert len(bridge) >= 2450, f"Se esperaban >= 2450 municipios en la tabla puente, encontrados: {len(bridge)}"
