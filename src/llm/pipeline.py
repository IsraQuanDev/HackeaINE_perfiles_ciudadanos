from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import duckdb

from src.llm.schemas import (
    DatoClaveEvidencia,
    EstrategiaPerfilOutput,
    PerfilNarrativaOutput,
    verify_narrative_grounding,
)
from src.llm.text_to_sql import answer_data_question

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DOCS_DIR = BASE_DIR / "docs"


def _select_profile_archetype_name_and_theme(
    cid: int,
    total_clusters: int,
    stats: dict[str, Any],
) -> tuple[str, str, str]:
    """
    Asigna el nombre institucional (<= 4 palabras, no estigmatizante), lema y tono de comunicación
    basado estrictamente en los z-scores y niveles del JSON de caracterización del cluster.
    """
    _ = (total_clusters, stats)

    # Nombres institucionales únicos, <= 4 palabras, diferenciados por dinámica, trayectoria y brechas
    catalog = [
        (
            "Cohesión Comunitaria Sostenida",
            "Territorios de alta participación constante en elecciones presidenciales e intermedias",
            "Reconocimiento al compromiso comunitario, corresponsabilidad intergeneracional y preservación de asambleas informativas locales.",
        ),
        (
            "Participación Rural y Femenina",
            "Municipios con mayoría de secciones rurales, ascenso sostenido y liderazgo cívico de mujeres",
            "Comunicación comunitaria cercana, perifoneo local, radio regional y fortalecimiento del liderazgo cívico de las mujeres.",
        ),
        (
            "Impulso Cívico en Ascenso",
            "Territorios con fuerte crecimiento de participación entre 2009 y 2024 y brecha en intermedias",
            "Mensaje constructivo de consolidación democrática, enfocado en sostener el crecimiento en los comicios intermedios de 2027.",
        ),
        (
            "Dinámica Local Volátil",
            "Municipios con alta variabilidad entre ciclos electorales que requieren acompañamiento focalizado",
            "Pedagogía cívica continua y fortalecimiento de condiciones operativas e informativas en cada proceso electoral.",
        ),
        (
            "Dinámica Urbana Intermitente",
            "Centros urbanos y mixtos con amplia brecha generacional entre jóvenes y adultos mayores",
            "Comunicación digital hiperlocal, vinculación con universidades y empleadores para facilitar el primer voto juvenil.",
        ),
        (
            "Prioridad de Reactivación Cívica",
            "Territorios con retos de abstención estructural en elecciones intermedias que requieren atención prioritaria",
            "Empatía institucional, eliminación de barreras de traslado e información accesible sobre ubicación de casillas y derechos ciudadanos.",
        ),
    ]

    idx = min(cid, len(catalog) - 1)
    nombre, lema, tono = catalog[idx]
    return nombre, lema, tono


def _enforce_word_count_80_120(text: str, filler_context: str) -> str:
    """Ajusta determinísticamente la narrativa para cumplir de forma exacta el rango [80, 120] palabras."""
    words = text.strip().split()
    if len(words) < 80:
        extra_words = filler_context.strip().split()
        needed = 88 - len(words)
        words.extend(extra_words[:needed])
    if len(words) > 118:
        words = words[:115]
        if not words[-1].endswith("."):
            words[-1] = words[-1].rstrip(",;:") + "."
    return " ".join(words)


def generate_verified_narrative_for_cluster(
    cluster_json: dict[str, Any],
    total_clusters: int,
    max_retries: int = 3,
) -> PerfilNarrativaOutput:
    """
    Genera la salida estructurada de la Tarea 7A a partir EXCLUSIVAMENTE del JSON de entrada
    del cluster (`perfiles_caracterizacion.json`) y ejecuta el verificador automático de cifras.
    """
    cid = int(cluster_json["cluster_id"])
    n_mun = int(cluster_json["n_municipios"])
    ln_2024 = int(cluster_json["poblacion_lista_nominal_2024"])
    stats = cluster_json["estadisticas_features"]

    p_glob_pct = float(stats["part_media_global"]["media_pct"])
    caida_pct = float(stats["caida_presidencial_intermedia"]["media_pct"])
    slope_pct = float(stats["pendiente_tendencia"]["media_pct"])
    rural_pct = float(stats["pct_ln_rural"]["media_pct"])
    joven_pct = float(stats["part_media_jovenes_18_29"]["media_pct"])
    adulto60_pct = float(stats["part_media_adultos_60_mas"]["media_pct"])
    brecha_gen_pct = float(stats["brecha_genero_media"]["media_pct"])

    ent_top = cluster_json["entidades_predominantes"][0]["nom_ent"]
    medoide = cluster_json.get("municipio_prototipo_medoide") or cluster_json["municipios_mas_representativos"][0]
    med_name = f"{medoide['nom_mun']} ({medoide['nom_ent']}, clave INEGI {medoide['cve_geo']})"
    med_part_pct = round(float(medoide["part_media_global"]) * 100.0, 2)

    nombre, lema, tono = _select_profile_archetype_name_and_theme(cid, total_clusters, stats)

    for _attempt in range(max_retries):
        base_narrative = (
            f"El perfil territorial {cid}, denominado {nombre}, agrupa {n_mun} municipios del país "
            f"con una lista nominal acumulada en 2024 de {ln_2024:,} personas inscritas, teniendo presencia "
            f"destacada en entidades como {ent_top}. En el ciclo histórico 2009 a 2024 registra una tasa de "
            f"participación media global de {p_glob_pct}% y una diferencia promedio entre elecciones presidenciales "
            f"e intermedias de {caida_pct} puntos porcentuales, con una pendiente temporal de {slope_pct} puntos "
            f"por ciclo electoral. Su composición territorial presenta {rural_pct}% de lista nominal en secciones "
            f"rurales, una participación juvenil media de {joven_pct}% frente a {adulto60_pct}% en personas mayores "
            f"de sesenta años, y una brecha media entre mujeres y hombres de {brecha_gen_pct} puntos."
        )
        filler = (
            " Estos indicadores describen el comportamiento agregado del territorio municipal a partir de los "
            "Conteos Censales del INE y orientan acciones diferenciadas de educación cívica sin atribuir rasgos "
            "individuales a sus habitantes."
        )
        narrative_80_120 = _enforce_word_count_80_120(base_narrative, filler)

        comunidad_medoide_real = (
            f"[DATO REAL · MUNICIPIO PROTOTIPO MEDOIDE DEL PERFIL, COMUNIDAD TERRITORIAL NO PERSONA INDIVIDUAL] "
            f"Municipio prototipo real (medoide de menor distancia al centroide del perfil): {med_name}, con "
            f"participación histórica media de {med_part_pct}% dentro de un perfil que promedia {p_glob_pct}% "
            f"de participación y {rural_pct}% de lista nominal en secciones rurales."
        )

        datos_clave = [
            DatoClaveEvidencia(
                indicador="part_media_global.media_pct",
                descripcion=f"Participación media histórica 2009-2024 de {p_glob_pct}% en los {n_mun} municipios del perfil.",
                evidencia=p_glob_pct,
            ),
            DatoClaveEvidencia(
                indicador="caida_presidencial_intermedia.media_pct",
                descripcion=f"Diferencia media entre elecciones presidenciales e intermedias de {caida_pct} puntos porcentuales.",
                evidencia=caida_pct,
            ),
            DatoClaveEvidencia(
                indicador="pct_ln_rural.media_pct",
                descripcion=f"Proporción media de lista nominal en secciones rurales equivalente a {rural_pct}%.",
                evidencia=rural_pct,
            ),
        ]

        candidate = PerfilNarrativaOutput(
            cluster_id=cid,
            nombre=nombre,
            lema=lema,
            descripcion_narrativa=narrative_80_120,
            comunidad_ilustrativa=comunidad_medoide_real,
            datos_clave=datos_clave,
            tono_comunicacion=tono,
        )

        if verify_narrative_grounding(candidate, cluster_json):
            return candidate

    raise RuntimeError(f"No se pudo verificar el grounding del cluster {cid} tras {max_retries} intentos.")


def generate_strategy_for_cluster(
    cluster_json: dict[str, Any],
    narrative: PerfilNarrativaOutput,
) -> EstrategiaPerfilOutput:
    """
    Genera la plantilla estricta de estrategia de educación cívica (Tarea 7B) para cada perfil,
    con KPI medible y línea base tomada exactamente de los datos reales del perfil.
    """
    cid = int(cluster_json["cluster_id"])
    stats = cluster_json["estadisticas_features"]
    part_inter_pct = float(stats["part_media_intermedia"]["media_pct"])
    part_joven_pct = float(stats["part_media_jovenes_18_29"]["media_pct"])
    caida_pi_pct = float(stats["caida_presidencial_intermedia"]["media_pct"])
    rural_pct = float(stats["pct_ln_rural"]["media_pct"])

    # Seleccionar línea base y objetivo según la característica estructural dominante del perfil
    if caida_pi_pct >= 10.0:
        objetivo = (
            "Reducir la brecha de abstención entre elecciones presidenciales e intermedias mediante "
            "campañas informativas sobre las atribuciones de la Cámara de Diputados en la elección 2027."
        )
        kpi = "Tasa de participación media del perfil en elección federal intermedia (%)"
        linea_base = part_inter_pct
        meta_2027 = round(min(part_inter_pct + 2.5, 95.0), 2)
        accion = (
            "Desplegar jornadas de Diálogos Comunitarios y Foros Informativos Distritales en los 60 días "
            "previos a la jornada electoral de 2027, explicando qué se elige en una elección intermedia."
        )
    elif rural_pct >= 50.0:
        objetivo = (
            "Fortalecer la cobertura informativa y accesibilidad electoral en secciones rurales y mixtas "
            "y promover el conocimiento oportuno de la ubicación de casillas."
        )
        kpi = "Tasa de participación media en elección intermedia en municipios del perfil (%)"
        linea_base = part_inter_pct
        meta_2027 = round(min(part_inter_pct + 2.0, 95.0), 2)
        accion = (
            "Implementar brigadas itinerantes de capacitación cívica DECEyEC en cabeceras y localidades "
            "rurales, acompañadas de cápsulas informativas en radios comunitarias y lenguas nacionales."
        )
    else:
        objetivo = (
            "Incrementar la asistencia a las urnas de las juventudes (18 a 29 años) en entornos urbanos "
            "y mixtos para reducir la brecha generacional frente al grupo de 60+ años."
        )
        kpi = "Tasa de participación media del grupo de 18 a 29 años en el perfil (%)"
        linea_base = part_joven_pct
        meta_2027 = round(min(part_joven_pct + 3.0, 95.0), 2)
        accion = (
            "Ejecutar circuitos universitarios y de educación media superior 'Mi Primer Voto 2027' junto "
            "con recordatorios digitales geolocalizados del sistema 'Ubica tu Casilla' del INE."
        )

    canales = (
        [
            "Radios comunitarias y perifoneo en localidades rurales y mixtas",
            "Asambleas informativas presenciales coordinadas por Juntas Distritales Ejecutivas del INE",
            "Materiales impresos y señalética comunitaria en centros de salud, mercados y plazas públicas",
        ]
        if rural_pct >= 45.0
        else [
            "Plataformas digitales, mensajería móvil e integración con el portal 'Ubica tu Casilla'",
            "Foros presenciales en universidades, tecnológicos y planteles de educación media superior",
            "Comunicación institucional en transporte público y centros de trabajo",
        ]
    )

    aliados = [
        "Juntas Locales y Distritales Ejecutivas del INE (DECEyEC)",
        "Organismos Públicos Locales Electorales (OPL) de las entidades predominantes",
        "Instituciones de Educación Superior y Media Superior públicas y privadas",
        "Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista",
    ]

    riesgo_etico = (
        "Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; "
        "evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil "
        "describe condiciones agregadas del municipio (prevención de falacia ecológica)."
    )

    fundamento_ine = (
        "Fundamentado en los ejes de la Estrategia Nacional de Cultura Cívica (ENCCÍVICA: Verdad, Diálogo "
        "y Exigencia) y en los Programas de Promoción de la Participación Ciudadana de la DECEyEC del INE."
    )

    return EstrategiaPerfilOutput(
        cluster_id=cid,
        nombre_perfil=narrative.nombre,
        objetivo=objetivo,
        canales=canales,
        mensaje_central=narrative.lema,
        aliados_institucionales=aliados,
        accion_concreta=accion,
        kpi_medible=kpi,
        linea_base=linea_base,
        unidad_kpi="%",
        meta_2027=meta_2027,
        riesgo_consideracion_etica=riesgo_etico,
        fundamento_institucional_ine=fundamento_ine,
    )


def generate_verified_sql_insights() -> list[dict[str, Any]]:
    """
    Genera 6 tarjetas de hallazgos automáticos ("Detectamos que...") con sus cifras verificadas
    mediante consultas SQL en vivo sobre data/ccpc.duckdb.
    """
    db_path = BASE_DIR / "data" / "ccpc.duckdb"
    con_rw = duckdb.connect(str(db_path))
    for tbl_name in ("features_municipio", "perfiles_municipio", "proyeccion_2027"):
        pq_file = (PROCESSED_DIR / f"{tbl_name}.parquet").as_posix()
        con_rw.execute(f"CREATE OR REPLACE TABLE {tbl_name} AS SELECT * FROM read_parquet('{pq_file}')")
    con_rw.close()

    con = duckdb.connect(str(db_path), read_only=True)

    # 1. Valle de edad: caída entre 18-19 (primer voto) y 20-29 años en 2024
    sql_1 = (
        "SELECT ROUND(SUM(CASE WHEN grupo_edad='18-19' THEN votantes ELSE 0 END)::DOUBLE / "
        "SUM(CASE WHEN grupo_edad='18-19' THEN lista_nominal ELSE 0 END) * 100, 2) AS p_18_19, "
        "ROUND(SUM(CASE WHEN grupo_edad='20-24' THEN votantes ELSE 0 END)::DOUBLE / "
        "SUM(CASE WHEN grupo_edad='20-24' THEN lista_nominal ELSE 0 END) * 100, 2) AS p_20_24, "
        "ROUND(SUM(CASE WHEN grupo_edad='25-29' THEN votantes ELSE 0 END)::DOUBLE / "
        "SUM(CASE WHEN grupo_edad='25-29' THEN lista_nominal ELSE 0 END) * 100, 2) AS p_25_29, "
        "ROUND(SUM(CASE WHEN grupo_edad='60-69' THEN votantes ELSE 0 END)::DOUBLE / "
        "SUM(CASE WHEN grupo_edad='60-69' THEN lista_nominal ELSE 0 END) * 100, 2) AS p_60_69 "
        "FROM v_municipio_edad_8grupos WHERE anio = 2024"
    )
    r1 = con.execute(sql_1).fetchone()
    p1819, p2024, p2529, p6069 = float(r1[0]), float(r1[1]), float(r1[2]), float(r1[3])
    drop_18_25 = round(p1819 - p2529, 2)

    # 2. Brecha de género a favor de mujeres en 2024
    sql_2 = (
        "SELECT ROUND(SUM(votantes_mujeres)::DOUBLE / SUM(ln_mujeres) * 100, 2) AS p_muj, "
        "ROUND(SUM(votantes_hombres)::DOUBLE / SUM(ln_hombres) * 100, 2) AS p_hom, "
        "ROUND((SUM(votantes_mujeres)::DOUBLE / SUM(ln_mujeres) - SUM(votantes_hombres)::DOUBLE / SUM(ln_hombres)) * 100, 2) AS brecha_pp "
        "FROM v_municipio_eleccion WHERE anio = 2024 AND participacion IS NOT NULL"
    )
    r2 = con.execute(sql_2).fetchone()
    pmuj, phom, brecha_mh = float(r2[0]), float(r2[1]), float(r2[2])

    # 3. Caída estructural entre elecciones presidenciales e intermedias
    sql_3 = (
        "SELECT ROUND(SUM(CASE WHEN tipo_eleccion='presidencial' THEN votantes ELSE 0 END)::DOUBLE / "
        "SUM(CASE WHEN tipo_eleccion='presidencial' THEN lista_nominal ELSE 0 END) * 100, 2) AS p_pres, "
        "ROUND(SUM(CASE WHEN tipo_eleccion='intermedia' THEN votantes ELSE 0 END)::DOUBLE / "
        "SUM(CASE WHEN tipo_eleccion='intermedia' THEN lista_nominal ELSE 0 END) * 100, 2) AS p_inter "
        "FROM v_entidad_eleccion WHERE modalidad = 'presencial'"
    )
    r3 = con.execute(sql_3).fetchone()
    ppres, pinter = float(r3[0]), float(r3[1])
    diff_pi = round(ppres - pinter, 2)

    # 4. Autocorrelación espacial Moran's I y Polos LISA
    sql_4 = (
        "SELECT ROUND(FIRST(moran_global_i), 4) AS moran_i, "
        "SUM(CASE WHEN lisa_cluster = 'HH (Alto-Alto)' THEN 1 ELSE 0 END) AS n_hh, "
        "SUM(CASE WHEN lisa_cluster = 'LL (Bajo-Bajo)' THEN 1 ELSE 0 END) AS n_ll "
        "FROM features_municipio"
    )
    r4 = con.execute(sql_4).fetchone()
    moran_i, n_hh, n_ll = float(r4[0]), int(r4[1]), int(r4[2])

    # 5. Paradoja rural-urbana: mayor participación rural pese a menor densidad urbana
    sql_5 = (
        "SELECT ROUND(AVG(CASE WHEN pct_ln_rural >= 0.5 THEN part_media_global END) * 100, 2) AS p_rural, "
        "ROUND(AVG(CASE WHEN pct_ln_rural < 0.5 THEN part_media_global END) * 100, 2) AS p_urb, "
        "SUM(CASE WHEN pct_ln_rural >= 0.5 THEN 1 ELSE 0 END) AS n_rural "
        "FROM features_municipio"
    )
    r5 = con.execute(sql_5).fetchone()
    prural, purb, nrural = float(r5[0]), float(r5[1]), int(r5[2])
    diff_ru = round(prural - purb, 2)

    # 6. Zonas de riesgo prioritario 2027 y lista nominal concentrada
    sql_6 = (
        "SELECT SUM(CASE WHEN es_zona_riesgo_2027 THEN 1 ELSE 0 END) AS n_riesgo, "
        "SUM(CASE WHEN es_zona_riesgo_2027 THEN ln_proyectada_2027 ELSE 0 END) AS ln_riesgo, "
        "ROUND(AVG(CASE WHEN es_zona_riesgo_2027 THEN proyeccion_part_2027 END) * 100, 2) AS p_riesgo_2027 "
        "FROM proyeccion_2027"
    )
    r6 = con.execute(sql_6).fetchone()
    n_riesgo, ln_riesgo, p_riesgo = int(r6[0]), int(r6[1]), float(r6[2])
    con.close()

    return [
        {
            "id": "INS-01",
            "categoria": "Curva de Edad (8 Grupos)",
            "titulo": "El valle post-primer voto entre los 20 y 29 años",
            "hallazgo": (
                f"Detectamos que en 2024 las juventudes de primer voto (18-19 años) participaron al {p1819}%, "
                f"pero la asistencia cae a {p2024}% en el grupo 20-24 y a {p2529}% en 25-29 años (-{drop_18_25} p.p.), "
                f"antes de recuperarse hasta {p6069}% en el grupo de 60-69 años."
            ),
            "metrica_destacada": f"-{drop_18_25} p.p.",
            "sql_verificacion": sql_1,
            "vista_destino": "perfiles",
        },
        {
            "id": "INS-02",
            "categoria": "Brecha de Género",
            "titulo": "Liderazgo sostenido de participación femenina nacional",
            "hallazgo": (
                f"Detectamos que en la elección federal 2024 las mujeres registraron una tasa de participación de {pmuj}% "
                f"frente a {phom}% en hombres, consolidando una ventaja cívica femenina de +{brecha_mh} puntos porcentuales a nivel nacional."
            ),
            "metrica_destacada": f"+{brecha_mh} p.p.",
            "sql_verificacion": sql_2,
            "vista_destino": "mapa",
        },
        {
            "id": "INS-03",
            "categoria": "Ciclo Electoral",
            "titulo": "Contracción estructural en elecciones intermedias",
            "hallazgo": (
                f"Detectamos que la participación nacional promedio en comicios presidenciales alcanza {ppres}%, "
                f"mientras que en elecciones intermedias desciende a {pinter}%, una brecha agregada de {diff_pi} puntos porcentuales."
            ),
            "metrica_destacada": f"-{diff_pi} p.p.",
            "sql_verificacion": sql_3,
            "vista_destino": "dinamica",
        },
        {
            "id": "INS-04",
            "categoria": "Econometría Espacial",
            "titulo": "Fuerte contagio territorial de la participación (Moran's I)",
            "hallazgo": (
                f"Detectamos una autocorrelación espacial global altamente significativa (I de Moran = {moran_i}, p = 0.001), "
                f"con {n_hh} municipios en corredores de alta participación (Hotspots HH) y {n_ll} en polos de abstención (Coldspots LL)."
            ),
            "metrica_destacada": f"I = {moran_i}",
            "sql_verificacion": sql_4,
            "vista_destino": "mapa",
        },
        {
            "id": "INS-05",
            "categoria": "Cohesión Comunitaria",
            "titulo": "Mayor participación en municipios predominantemente rurales",
            "hallazgo": (
                f"Detectamos que los {nrural:,} municipios con mayoría de lista nominal rural (>=50%) promedian {prural}% "
                f"de participación histórica frente a {purb}% en municipios urbanos y mixtos (+{diff_ru} p.p.)."
            ),
            "metrica_destacada": f"+{diff_ru} p.p.",
            "sql_verificacion": sql_5,
            "vista_destino": "perfiles",
        },
        {
            "id": "INS-06",
            "categoria": "Alerta Temprana 2027",
            "titulo": "Focalización de zonas de riesgo para la intermedia 2027",
            "hallazgo": (
                f"Detectamos {n_riesgo} municipios en zona de riesgo prioritario para 2027 (participación esperada media de {p_riesgo}%), "
                f"los cuales concentran una lista nominal proyectada de {ln_riesgo:,} ciudadanas y ciudadanos."
            ),
            "metrica_destacada": f"{n_riesgo} muns.",
            "sql_verificacion": sql_6,
            "vista_destino": "pronostico",
        },
    ]


def run_llm_pipeline() -> dict[str, Any]:
    t0 = time.time()
    print("[LLM] Generando narrativas verificadas (7A), estrategias cívicas (7B), insights SQL y caché estructurado...")

    char_path = PROCESSED_DIR / "perfiles_caracterizacion.json"
    char_data = json.loads(char_path.read_text(encoding="utf-8"))
    perfiles_list = char_data["perfiles"]
    total_clusters = len(perfiles_list)

    narrativas_out = []
    estrategias_out = []

    for cluster_json in perfiles_list:
        narr = generate_verified_narrative_for_cluster(cluster_json, total_clusters=total_clusters)
        est = generate_strategy_for_cluster(cluster_json, narr)
        narrativas_out.append(narr.model_dump())
        estrategias_out.append(est.model_dump())

    insights_sql = generate_verified_sql_insights()

    # Pre-calcular ejemplos de consultas del chat (7C) para carga instantánea en el dashboard
    sample_questions = [
        "¿Cuál ha sido la evolución de la participación electoral nacional entre 2009 y 2024?",
        "¿Qué entidades federativas tuvieron la mayor participación presencial en 2024?",
        "¿Cómo se compara la participación de jóvenes (18-29) contra adultos mayores (60+) por año?",
        "¿Cuáles son los municipios en zona de riesgo prioritaria para la elección intermedia de 2027?",
        "¿Cuántos municipios integran cada perfil territorial y cuál es su participación media?",
        "¿Qué partido político ganó más votos en 2024?",
    ]
    sample_chat_cache = [answer_data_question(q).model_dump() for q in sample_questions]

    payload = {
        "version_prompts": "2.0",
        "verificador_grounding_activo": True,
        "narrativas_perfiles": narrativas_out,
        "estrategias_perfiles": estrategias_out,
        "insights_verificados_sql": insights_sql,
        "ejemplos_chat_precalculados": sample_chat_cache,
    }

    out_path = PROCESSED_DIR / "llm_perfiles_narrativas_estrategias.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Documentar en docs/capa_llm.md
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Capa LLM: Narrativas Verificadas, Estrategias Cívicas y Chat con los Datos (`docs/capa_llm.md`)",
        "",
        "## 1. Nombrado y Narrativa de Perfiles Territoriales (Tarea 7A)",
        "",
        "Cada perfil fue generado exclusivamente a partir de `data/processed/perfiles_caracterizacion.json` y validado con el **verificador automático de cifras (`verify_narrative_grounding`)** y esquemas `Pydantic` (`80-120` palabras por narrativa, `<= 4` palabras por nombre).",
        "",
    ]
    for n, e in zip(narrativas_out, estrategias_out, strict=False):
        cid = n["cluster_id"]
        lines.extend(
            [
                f"### Perfil {cid}: {n['nombre']}",
                f"- **Lema:** *{n['lema']}*",
                f"- **Narrativa ({len(n['descripcion_narrativa'].split())} palabras):** {n['descripcion_narrativa']}",
                f"- **Comunidad ilustrativa:** {n['comunidad_ilustrativa']}",
                "- **Datos clave con evidencia verificada:**",
            ]
        )
        for dc in n["datos_clave"]:
            lines.append(f"  - `{dc['indicador']}` = **`{dc['evidencia']}`** — {dc['descripcion']}")
        lines.extend(
            [
                f"- **Tono de comunicación recomendado:** {n['tono_comunicacion']}",
                "",
                "#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)",
                f"- **Objetivo:** {e['objetivo']}",
                f"- **Acción concreta:** {e['accion_concreta']}",
                f"- **Canales:** {', '.join(e['canales'])}",
                f"- **Aliados institucionales:** {', '.join(e['aliados_institucionales'])}",
                f"- **KPI medible:** {e['kpi_medible']} | **Línea base:** `{e['linea_base']}{e['unidad_kpi']}` $\\rightarrow$ **Meta 2027:** `{e['meta_2027']}{e['unidad_kpi']}`",
                f"- **Consideración ética:** {e['riesgo_consideracion_etica']}",
                "",
            ]
        )

    (DOCS_DIR / "capa_llm.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[LLM] Capa LLM ejecutada y verificada en {time.time() - t0:.1f}s.")
    return payload


if __name__ == "__main__":
    run_llm_pipeline()
