from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Any

import duckdb
import yaml

from src.llm.schemas import ChatSQLResponse

BASE_DIR = Path(__file__).resolve().parents[2]
DUCKDB_PATH = BASE_DIR / "data" / "ccpc.duckdb"
SEMANTIC_PATH = BASE_DIR / "docs" / "capa_semantica.yaml"


def _strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def load_semantic_layer() -> dict[str, Any]:
    return yaml.safe_load(SEMANTIC_PATH.read_text(encoding="utf-8"))


def validate_safe_sql(sql: str, semantic: dict[str, Any]) -> str:
    """
    Valida que la sentencia SQL cumpla estrictamente con:
    1) Solo SELECT (o WITH ... SELECT).
    2) Sin palabras prohibidas (DDL/DML/administración).
    3) Solo tablas de la lista blanca (whitelist).
    4) Límite máximo de filas (<= 100).
    """
    cleaned = sql.strip().rstrip(";")
    upper_sql = cleaned.upper()

    if not (upper_sql.startswith("SELECT") or upper_sql.startswith("WITH")):
        raise ValueError("Seguridad SQL: Solo se permiten consultas SELECT de solo lectura.")

    if ";" in cleaned:
        raise ValueError("Seguridad SQL: No se permiten múltiples sentencias SQL separadas por punto y coma.")

    forbidden: list[str] = semantic["limites_seguridad"]["palabras_prohibidas"]
    for word in forbidden:
        if re.search(rf"\b{word}\b", upper_sql):
            raise ValueError(f"Seguridad SQL: Palabra reservada prohibida detectada: {word}")

    whitelist = {t.lower() for t in semantic["whitelist_tables"]}
    # Extraer nombres de CTEs definidas en WITH nombre AS (...)
    cte_names = {
        m.lower() for m in re.findall(r"\bWITH\s+([a-zA-Z0-9_]+)\s+AS|\b,\s*([a-zA-Z0-9_]+)\s+AS", cleaned, flags=re.IGNORECASE)
        for m in m if m
    }
    referenced = [
        m.lower()
        for m in re.findall(r"\b(?:FROM|JOIN)\s+([a-zA-Z0-9_]+)\b", cleaned, flags=re.IGNORECASE)
    ]
    for tbl in referenced:
        if tbl not in whitelist and tbl not in cte_names:
            raise ValueError(f"Seguridad SQL: Tabla '{tbl}' no pertenece a la lista blanca autorizada.")

    max_rows = int(semantic["limites_seguridad"]["max_filas"])
    if "LIMIT" not in upper_sql:
        cleaned = f"{cleaned} LIMIT {max_rows}"
    return cleaned


ENTIDADES_MAP = {
    "aguascalientes": "Aguascalientes",
    "baja california sur": "Baja California Sur",
    "baja california": "Baja California",
    "campeche": "Campeche",
    "coahuila": "Coahuila",
    "colima": "Colima",
    "chiapas": "Chiapas",
    "chihuahua": "Chihuahua",
    "ciudad de mexico": "Ciudad de México",
    "cdmx": "Ciudad de México",
    "distrito federal": "Ciudad de México",
    "durango": "Durango",
    "guanajuato": "Guanajuato",
    "guerrero": "Guerrero",
    "hidalgo": "Hidalgo",
    "jalisco": "Jalisco",
    "estado de mexico": "Estado de México",
    "edomex": "Estado de México",
    "michoacan": "Michoacán",
    "morelos": "Morelos",
    "nayarit": "Nayarit",
    "nuevo leon": "Nuevo León",
    "oaxaca": "Oaxaca",
    "puebla": "Puebla",
    "queretaro": "Querétaro",
    "quintana roo": "Quintana Roo",
    "san luis potosi": "San Luis Potosí",
    "sinaloa": "Sinaloa",
    "sonora": "Sonora",
    "tabasco": "Tabasco",
    "tamaulipas": "Tamaulipas",
    "tlaxcala": "Tlaxcala",
    "veracruz": "Veracruz",
    "yucatan": "Yucatán",
    "zacatecas": "Zacatecas",
}


def _detect_unanswerable(q_norm: str) -> str | None:
    """Detecta preguntas que requieren datos fuera del alcance del CCPC o violan principios éticos."""
    unanswerable_triggers = [
        (
            r"\b(partido|morena|pan|pri|prd|mc|pvem|pt|candidat|quien gano|ganador|preferencia electoral|voto nulo|boleta)\b",
            "No es posible responder esta pregunta con los datos del proyecto. Los Conteos Censales de Participación Ciudadana (CCPC) del INE provienen de los cuadernillos de la Lista Nominal (si la persona asistió o no a votar) y no contienen resultados por partido político, candidaturas ni sentido del voto.",
        ),
        (
            r"\b(nombre de la persona|curp|clave de elector|domicilio|quien voto|individuo especifico|reidentificar|datos personales)\b",
            "Solicitud rechazada por el Principio Inquebrantable #1 (Privacidad y Datos Agregados): el sistema opera exclusivamente con conteos estadísticos agregados por territorio y prohíbe cualquier intento de consulta o reidentificación individual.",
        ),
        (
            r"\b(religion|ingreso mensual|salario|preferencia sexual|afiliacion sindical|encuesta de salida)\b",
            "No es posible responder esta pregunta con los datos disponibles. El catálogo CCPC del INE no registra variables de religión, ingresos individuales ni encuestas de salida.",
        ),
        (
            r"\b(casillas especiales|voto en el extranjero|residentes en el extranjero)\b",
            "Como documenta oficialmente la DECEyEC en los diccionarios de datos CCPC 2009-2024, los conteos censales se construyen a partir de los cuadernillos de casillas ordinarias aprobadas por los consejos distritales y no contemplan casillas especiales ni voto desde el extranjero.",
        ),
    ]
    for pattern, reason in unanswerable_triggers:
        if re.search(pattern, q_norm):
            return reason
    return None


def _compile_question_to_sql(question: str) -> tuple[str | None, str]:
    """
    Traduce preguntas en lenguaje natural a SQL sobre DuckDB utilizando la capa semántica
    (`docs/capa_semantica.yaml`). Retorna (sql, chart_type).
    """
    q_norm = _strip_accents(question.lower().strip())

    # Extraer año si se menciona (2009, 2012, 2015, 2018, 2021, 2024, 2027)
    years_found = [int(y) for y in re.findall(r"\b(2009|2012|2015|2018|2021|2024|2027)\b", q_norm)]
    year = years_found[0] if years_found else None

    # Extraer entidad si se menciona
    detected_ent = None
    for k_ent in sorted(ENTIDADES_MAP.keys(), key=len, reverse=True):
        if re.search(rf"\b{re.escape(k_ent)}\b", q_norm):
            detected_ent = ENTIDADES_MAP[k_ent]
            break

    # 1. Modalidad Prisión Preventiva 2024
    if "prision preventiva" in q_norm:
        if detected_ent:
            return (
                f"SELECT anio, nom_ent, SUM(votantes) AS votantes_prision_preventiva "
                f"FROM v_entidad_eleccion WHERE modalidad = 'prision_preventiva' AND nom_ent = '{detected_ent}' "
                f"GROUP BY anio, nom_ent LIMIT 10",
                "bar",
            )
        return (
            "SELECT SUM(votantes) AS total_votantes_prision_preventiva, COUNT(DISTINCT cve_ent) AS entidades_con_registro "
            "FROM v_entidad_eleccion WHERE modalidad = 'prision_preventiva' AND votantes > 0 LIMIT 10",
            "kpi",
        )

    # 2. Modalidad Voto Anticipado 2024
    if "voto anticipado" in q_norm or "anticipado" in q_norm:
        if "municipio" in q_norm or "tasa" in q_norm:
            return (
                "SELECT cve_geo, nom_mun, nom_ent, votantes_anticipado_2024, ROUND(tasa_voto_anticipado_por_10k, 2) AS tasa_por_10k_ln "
                "FROM features_municipio ORDER BY votantes_anticipado_2024 DESC LIMIT 10",
                "bar",
            )
        if detected_ent:
            return (
                f"SELECT nom_ent, SUM(votantes) AS votantes_anticipado_2024 "
                f"FROM v_entidad_eleccion WHERE modalidad = 'anticipado' AND nom_ent = '{detected_ent}' "
                f"GROUP BY nom_ent LIMIT 10",
                "kpi",
            )
        return (
            "SELECT SUM(votantes) AS total_votantes_anticipado_2024 "
            "FROM v_entidad_eleccion WHERE modalidad = 'anticipado' LIMIT 10",
            "kpi",
        )

    # 3. Proyección 2027 / Zonas en riesgo
    if year == 2027 or "2027" in q_norm or "zona de riesgo" in q_norm or "zonas en riesgo" in q_norm or "proyeccion" in q_norm:
        if "riesgo" in q_norm:
            ent_filter = f"AND nom_ent = '{detected_ent}' " if detected_ent else ""
            return (
                f"SELECT cve_geo, nom_mun, nom_ent, cluster_id, ln_proyectada_2027, "
                f"ROUND(proyeccion_part_2027 * 100, 2) AS proyeccion_2027_pct, indice_riesgo_priorizacion "
                f"FROM proyeccion_2027 WHERE es_zona_riesgo_2027 = true {ent_filter}"
                f"ORDER BY indice_riesgo_priorizacion DESC LIMIT 15",
                "bar",
            )
        if "perfil" in q_norm or "cluster" in q_norm:
            return (
                "SELECT cluster_id, COUNT(*) AS n_municipios, SUM(ln_proyectada_2027) AS ln_2027, "
                "ROUND(AVG(proyeccion_part_2027) * 100, 2) AS part_media_proyectada_2027_pct "
                "FROM proyeccion_2027 GROUP BY cluster_id ORDER BY cluster_id LIMIT 10",
                "bar",
            )
        return (
            "SELECT SUM(ln_proyectada_2027) AS ln_nacional_2027, SUM(votantes_esperados_2027) AS votantes_esperados_2027, "
            "ROUND(SUM(votantes_esperados_2027)::DOUBLE / SUM(ln_proyectada_2027) * 100, 2) AS participacion_proyectada_2027_pct, "
            "SUM(CASE WHEN es_zona_riesgo_2027 THEN 1 ELSE 0 END) AS municipios_en_riesgo "
            "FROM proyeccion_2027 LIMIT 5",
            "kpi",
        )

    # 4. Autocorrelación espacial / Moran / LISA
    if "moran" in q_norm or "lisa" in q_norm or "autocorrelacion espacial" in q_norm:
        return (
            "SELECT lisa_cluster, COUNT(*) AS n_municipios, ROUND(AVG(part_media_global) * 100, 2) AS part_media_pct, "
            "ROUND(FIRST(moran_global_i), 4) AS moran_global_i "
            "FROM features_municipio GROUP BY lisa_cluster ORDER BY n_municipios DESC LIMIT 10",
            "bar",
        )

    # 5. Cambios de marco geográfico / nuevos municipios / tabla puente
    if "nueva creacion" in q_norm or "nuevos municipios" in q_norm or "puente" in q_norm or "panel completo" in q_norm:
        return (
            "SELECT estatus_marco_geografico, COUNT(*) AS n_municipios, MIN(primer_anio) AS primer_anio_min "
            "FROM puente_municipio_anio GROUP BY estatus_marco_geografico ORDER BY n_municipios DESC LIMIT 15",
            "table",
        )

    # 6. Preguntas sobre Perfiles / Clusters
    if "perfil" in q_norm or "cluster" in q_norm or "segment" in q_norm:
        if detected_ent:
            return (
                f"SELECT p.cluster_id, COUNT(*) AS n_municipios, "
                f"ROUND(AVG(f.part_media_global) * 100, 2) AS part_media_pct "
                f"FROM perfiles_municipio p JOIN features_municipio f ON p.cve_geo = f.cve_geo "
                f"WHERE p.nom_ent = '{detected_ent}' GROUP BY p.cluster_id ORDER BY n_municipios DESC LIMIT 10",
                "bar",
            )
        return (
            "SELECT p.cluster_id, COUNT(*) AS n_municipios, SUM(f.ln_2024) AS lista_nominal_2024, "
            "ROUND(AVG(f.part_media_global) * 100, 2) AS part_media_pct, "
            "ROUND(AVG(f.caida_presidencial_intermedia) * 100, 2) AS caida_pres_inter_pp, "
            "ROUND(AVG(f.brecha_genero_media) * 100, 2) AS brecha_genero_pp "
            "FROM perfiles_municipio p JOIN features_municipio f ON p.cve_geo = f.cve_geo "
            "GROUP BY p.cluster_id ORDER BY p.cluster_id LIMIT 10",
            "table",
        )

    # 7. Brecha de género (mujeres vs hombres)
    if "mujeres" in q_norm or "hombres" in q_norm or "genero" in q_norm or "sexo" in q_norm:
        if year:
            ent_where = f"AND nom_ent = '{detected_ent}' " if detected_ent else ""
            return (
                f"SELECT anio, ROUND(SUM(votantes_mujeres)::DOUBLE / SUM(ln_mujeres) * 100, 2) AS part_mujeres_pct, "
                f"ROUND(SUM(votantes_hombres)::DOUBLE / SUM(ln_hombres) * 100, 2) AS part_hombres_pct, "
                f"ROUND((SUM(votantes_mujeres)::DOUBLE / SUM(ln_mujeres) - SUM(votantes_hombres)::DOUBLE / SUM(ln_hombres)) * 100, 2) AS brecha_m_h_pp "
                f"FROM v_municipio_eleccion WHERE anio = {year} {ent_where}GROUP BY anio LIMIT 10",
                "bar",
            )
        return (
            "SELECT cve_geo, nom_mun, nom_ent, ROUND(brecha_genero_media * 100, 2) AS brecha_mujeres_vs_hombres_pp, "
            "ROUND(part_media_global * 100, 2) AS part_media_pct "
            "FROM features_municipio ORDER BY brecha_genero_media DESC LIMIT 10",
            "bar",
        )

    # 8. Jóvenes (18-29) vs Adultos mayores (60+) / Edad
    if "joven" in q_norm or "18-29" in q_norm or "18 a 29" in q_norm or "60+" in q_norm or "adultos mayores" in q_norm or "edad" in q_norm or "generacional" in q_norm:
        if year:
            return (
                f"SELECT anio, ROUND(SUM(vot_18_29)::DOUBLE / SUM(ln_18_29) * 100, 2) AS part_jovenes_18_29_pct, "
                f"ROUND(SUM(vot_30_59)::DOUBLE / SUM(ln_30_59) * 100, 2) AS part_adultos_30_59_pct, "
                f"ROUND(SUM(vot_60_mas)::DOUBLE / SUM(ln_60_mas) * 100, 2) AS part_adultos_60_mas_pct "
                f"FROM v_municipio_eleccion WHERE anio = {year} GROUP BY anio LIMIT 10",
                "bar",
            )
        return (
            "SELECT anio, ROUND(SUM(vot_18_29)::DOUBLE / SUM(ln_18_29) * 100, 2) AS part_jovenes_18_29_pct, "
            "ROUND(SUM(vot_60_mas)::DOUBLE / SUM(ln_60_mas) * 100, 2) AS part_60_mas_pct, "
            "ROUND((SUM(vot_60_mas)::DOUBLE / SUM(ln_60_mas) - SUM(vot_18_29)::DOUBLE / SUM(ln_18_29)) * 100, 2) AS brecha_60_vs_18_29_pp "
            "FROM v_municipio_eleccion GROUP BY anio ORDER BY anio LIMIT 10",
            "line",
        )

    # 9. Secciones urbanas vs rurales
    if "rural" in q_norm or "urbana" in q_norm or "urbano" in q_norm or "tipo de seccion" in q_norm:
        return (
            "SELECT CASE WHEN pct_ln_rural >= 0.5 THEN 'Predominante Rural (>=50%)' ELSE 'Predominante Urbano/Mixto (<50% rural)' END AS tipo_municipio, "
            "COUNT(*) AS n_municipios, ROUND(AVG(part_media_global) * 100, 2) AS part_media_pct, "
            "ROUND(AVG(caida_presidencial_intermedia) * 100, 2) AS caida_pres_inter_pp "
            "FROM features_municipio GROUP BY 1 ORDER BY n_municipios DESC LIMIT 10",
            "bar",
        )

    # 10. Caída presidencial -> intermedia o comparativa presidencial vs intermedia
    if "caida" in q_norm or ("presidencial" in q_norm and "intermedia" in q_norm):
        if "municipio" in q_norm:
            return (
                "SELECT cve_geo, nom_mun, nom_ent, ROUND(part_media_presidencial * 100, 2) AS part_pres_pct, "
                "ROUND(part_media_intermedia * 100, 2) AS part_inter_pct, "
                "ROUND(caida_presidencial_intermedia * 100, 2) AS caida_pp "
                "FROM features_municipio ORDER BY caida_presidencial_intermedia DESC LIMIT 10",
                "bar",
            )
        return (
            "SELECT tipo_eleccion, COUNT(DISTINCT anio) AS n_elecciones, "
            "ROUND(SUM(votantes)::DOUBLE / SUM(lista_nominal) * 100, 2) AS participacion_nacional_pct "
            "FROM v_entidad_eleccion WHERE modalidad = 'presencial' GROUP BY tipo_eleccion ORDER BY participacion_nacional_pct DESC LIMIT 10",
            "bar",
        )

    # 11. Pendiente / tendencia creciente o decreciente / volatilidad
    if "creciente" in q_norm or "decreciente" in q_norm or "tendencia" in q_norm or "pendiente" in q_norm:
        order_dir = "ASC" if ("decreciente" in q_norm or "caida" in q_norm or "menor" in q_norm) else "DESC"
        return (
            f"SELECT cve_geo, nom_mun, nom_ent, ROUND(part_2009 * 100, 2) AS part_2009_pct, "
            f"ROUND(part_2024 * 100, 2) AS part_2024_pct, ROUND(pendiente_tendencia * 100, 2) AS pendiente_pp_por_ciclo "
            f"FROM features_municipio WHERE flag_baja_confiabilidad = false ORDER BY pendiente_tendencia {order_dir} LIMIT 10",
            "bar",
        )

    if "volatilidad" in q_norm or "inestable" in q_norm or "constancia" in q_norm:
        return (
            "SELECT cve_geo, nom_mun, nom_ent, ROUND(volatilidad * 100, 2) AS volatilidad_pp, "
            "ROUND(constancia_sobre_mediana * 100, 2) AS constancia_pct "
            "FROM features_municipio ORDER BY volatilidad DESC LIMIT 10",
            "bar",
        )

    # 12. Consultas por municipio o top/bottom municipios
    if "municipio" in q_norm or "municipios" in q_norm:
        order_dir = "ASC" if ("menor" in q_norm or "mas baja" in q_norm or "peor" in q_norm or "abstencion" in q_norm) else "DESC"
        ent_clause = f"WHERE nom_ent = '{detected_ent}' " if detected_ent else ""
        if year:
            where_y = f"WHERE anio = {year} " + (f"AND nom_ent = '{detected_ent}' " if detected_ent else "")
            return (
                f"SELECT cve_geo, nom_mun, nom_ent, anio, lista_nominal, votantes, "
                f"ROUND(participacion * 100, 2) AS participacion_pct "
                f"FROM v_municipio_eleccion {where_y}ORDER BY participacion {order_dir} LIMIT 10",
                "bar",
            )
        return (
            f"SELECT cve_geo, nom_mun, nom_ent, ln_2024, ROUND(part_media_global * 100, 2) AS part_media_2009_2024_pct "
            f"FROM features_municipio {ent_clause}ORDER BY part_media_global {order_dir} LIMIT 10",
            "bar",
        )

    # 13. Consultas por Entidad Federativa y/o Año específico
    if detected_ent and year:
        return (
            f"SELECT anio, nom_ent, lista_nominal, votantes, ROUND(participacion * 100, 2) AS participacion_pct "
            f"FROM v_entidad_eleccion WHERE modalidad = 'presencial' AND nom_ent = '{detected_ent}' AND anio = {year} LIMIT 10",
            "kpi",
        )

    if detected_ent and not year:
        return (
            f"SELECT anio, tipo_eleccion, nom_ent, lista_nominal, votantes, ROUND(participacion * 100, 2) AS participacion_pct "
            f"FROM v_entidad_eleccion WHERE modalidad = 'presencial' AND nom_ent = '{detected_ent}' ORDER BY anio LIMIT 10",
            "line",
        )

    if year and ("entidad" in q_norm or "estado" in q_norm or "mayor" in q_norm or "menor" in q_norm or "mas alta" in q_norm or "mas baja" in q_norm):
        order_dir = "ASC" if ("menor" in q_norm or "mas baja" in q_norm or "abstencion" in q_norm) else "DESC"
        return (
            f"SELECT cve_ent, nom_ent, lista_nominal, votantes, ROUND(participacion * 100, 2) AS participacion_pct "
            f"FROM v_entidad_eleccion WHERE modalidad = 'presencial' AND anio = {year} "
            f"ORDER BY participacion {order_dir} LIMIT 32",
            "bar",
        )

    if year:
        return (
            f"SELECT anio, SUM(lista_nominal) AS lista_nominal_nacional, SUM(votantes) AS votantes_nacional, "
            f"ROUND(SUM(votantes)::DOUBLE / SUM(lista_nominal) * 100, 2) AS participacion_nacional_pct "
            f"FROM v_entidad_eleccion WHERE modalidad = 'presencial' AND anio = {year} GROUP BY anio LIMIT 5",
            "kpi",
        )

    # 14. Evolución histórica nacional 2009-2024 (por defecto cuando pregunta por evolución/serie nacional)
    return (
        "SELECT anio, tipo_eleccion, SUM(lista_nominal) AS lista_nominal_nacional, SUM(votantes) AS votantes_nacional, "
        "ROUND(SUM(votantes)::DOUBLE / SUM(lista_nominal) * 100, 2) AS participacion_nacional_pct "
        "FROM v_entidad_eleccion WHERE modalidad = 'presencial' GROUP BY anio, tipo_eleccion ORDER BY anio LIMIT 10",
        "line",
    )


def answer_data_question(question: str) -> ChatSQLResponse:
    """
    Agente 'Pregúntale a los datos' (Prompt 7C):
    Verifica primero si la pregunta es respondible con el catálogo CCPC; si lo es,
    valida la consulta SQL contra la lista blanca y solo-SELECT, la ejecuta en DuckDB
    y construye la respuesta en lenguaje natural respaldada por las cifras exactas.
    """
    semantic = load_semantic_layer()
    q_norm = _strip_accents(question.lower().strip())

    refusal_reason = _detect_unanswerable(q_norm)
    if refusal_reason is not None:
        return ChatSQLResponse(
            pregunta=question,
            es_respondible=False,
            respuesta_natural=refusal_reason,
            sql_usado=None,
            tabla_respaldo=[],
            tipo_grafica_sugerida="none",
        )

    raw_sql, chart_type = _compile_question_to_sql(question)
    if raw_sql is None:
        return ChatSQLResponse(
            pregunta=question,
            es_respondible=False,
            respuesta_natural="La pregunta no puede responderse con las tablas disponibles en el catálogo CCPC 2009-2024.",
            sql_usado=None,
            tabla_respaldo=[],
            tipo_grafica_sugerida="none",
        )

    safe_sql = validate_safe_sql(raw_sql, semantic)

    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    df_res = con.execute(safe_sql).df()
    con.close()

    rows = df_res.to_dict(orient="records")
    if not rows:
        natural_reply = "La consulta se ejecutó correctamente pero no devolvió registros para los filtros solicitados."
    else:
        first_row = rows[0]
        kv_summary = ", ".join(f"{k}={v}" for k, v in first_row.items())
        natural_reply = (
            f"Consulta verificada sobre el catálogo DuckDB ({len(rows)} fila(s) recuperadas). "
            f"Resultado principal: {kv_summary}."
        )

    return ChatSQLResponse(
        pregunta=question,
        es_respondible=True,
        respuesta_natural=natural_reply,
        sql_usado=safe_sql,
        tabla_respaldo=rows,
        tipo_grafica_sugerida=chart_type,
    )
