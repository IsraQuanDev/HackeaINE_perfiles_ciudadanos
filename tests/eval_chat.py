from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.llm.schemas import (
    DatoClaveEvidencia,
    PerfilNarrativaOutput,
    verify_narrative_grounding,
)
from src.llm.text_to_sql import (
    answer_data_question,
    load_semantic_layer,
    validate_safe_sql,
)

BASE_DIR = Path(__file__).resolve().parents[1]
CHAR_PATH = BASE_DIR / "data" / "processed" / "perfiles_caracterizacion.json"
LLM_CACHE_PATH = BASE_DIR / "data" / "processed" / "llm_perfiles_narrativas_estrategias.json"

# Conjunto de evaluación de 30 preguntas con criterios esperados verificables (Prompt 7C)
EVAL_QUESTIONS_30 = [
    # 1-6: Totales y participación nacional por año
    {"id": 1, "q": "¿Cuál fue la participación electoral nacional presencial en 2009?", "respondible": True, "must_contain_col": "participacion_nacional_pct"},
    {"id": 2, "q": "¿Cuál fue la participación electoral nacional presencial en 2012?", "respondible": True, "must_contain_col": "participacion_nacional_pct"},
    {"id": 3, "q": "¿Cuál fue la participación electoral nacional presencial en 2015?", "respondible": True, "must_contain_col": "participacion_nacional_pct"},
    {"id": 4, "q": "¿Cuál fue la participación electoral nacional presencial en 2018?", "respondible": True, "must_contain_col": "participacion_nacional_pct"},
    {"id": 5, "q": "¿Cuál fue la participación electoral nacional presencial en 2021?", "respondible": True, "must_contain_col": "participacion_nacional_pct"},
    {"id": 6, "q": "¿Cuál fue la participación electoral nacional presencial en 2024?", "respondible": True, "must_contain_col": "participacion_nacional_pct"},
    # 7-11: Entidades federativas específicas y rankings estatales
    {"id": 7, "q": "¿Qué entidades tuvieron la mayor participación electoral en 2024?", "respondible": True, "must_contain_col": "participacion_pct"},
    {"id": 8, "q": "¿Qué estados tuvieron la menor participación en 2021?", "respondible": True, "must_contain_col": "participacion_pct"},
    {"id": 9, "q": "¿Cuál fue la participación en Yucatán en 2024?", "respondible": True, "must_contain_col": "participacion_pct"},
    {"id": 10, "q": "¿Cómo evolucionó la participación electoral en Ciudad de México de 2009 a 2024?", "respondible": True, "must_contain_col": "participacion_pct"},
    {"id": 11, "q": "¿Cuál fue la participación en Aguascalientes en 2018?", "respondible": True, "must_contain_col": "participacion_pct"},
    # 12-15: Municipios, tendencias, volatilidad y caída presidencial -> intermedia
    {"id": 12, "q": "¿Cuáles son los municipios con mayor participación promedio histórica?", "respondible": True, "must_contain_col": "part_media_2009_2024_pct"},
    {"id": 13, "q": "¿Cuáles son los municipios con menor participación electoral en 2024?", "respondible": True, "must_contain_col": "participacion_pct"},
    {"id": 14, "q": "¿Qué municipios presentan la mayor tendencia creciente de participación entre 2009 y 2024?", "respondible": True, "must_contain_col": "pendiente_pp_por_ciclo"},
    {"id": 15, "q": "¿Cómo se compara la participación nacional entre elecciones presidenciales e intermedias?", "respondible": True, "must_contain_col": "participacion_nacional_pct"},
    # 16-19: Género, Edad / Generacional y Ruralidad
    {"id": 16, "q": "¿Cuál fue la participación de mujeres y hombres en 2024 y su brecha?", "respondible": True, "must_contain_col": "brecha_m_h_pp"},
    {"id": 17, "q": "¿Cómo se compara la participación de jóvenes de 18 a 29 años frente a adultos mayores de 60+ en 2024?", "respondible": True, "must_contain_col": "part_jovenes_18_29_pct"},
    {"id": 18, "q": "¿Cuál ha sido la brecha generacional entre 60+ y 18-29 por año electoral?", "respondible": True, "must_contain_col": "brecha_60_vs_18_29_pp"},
    {"id": 19, "q": "¿Cómo difiere la participación media entre municipios predominantemente rurales y urbanos?", "respondible": True, "must_contain_col": "tipo_municipio"},
    # 20-21: Modalidades especiales 2024 (Voto Anticipado y Prisión Preventiva)
    {"id": 20, "q": "¿Cuántas personas votaron en la modalidad de voto anticipado en 2024?", "respondible": True, "must_contain_col": "total_votantes_anticipado_2024"},
    {"id": 21, "q": "¿Cuántos votantes se registraron en prisión preventiva en 2024?", "respondible": True, "must_contain_col": "total_votantes_prision_preventiva"},
    # 22-25: Perfiles, Proyección 2027, Zonas en riesgo, Moran/LISA y Tabla Puente
    {"id": 22, "q": "¿Cuántos municipios hay en cada perfil territorial y cuál es su participación media?", "respondible": True, "must_contain_col": "cluster_id"},
    {"id": 23, "q": "¿Cuál es la proyección nacional de participación y votantes para 2027?", "respondible": True, "must_contain_col": "participacion_proyectada_2027_pct"},
    {"id": 24, "q": "¿Cuáles son los principales municipios en zona de riesgo para 2027?", "respondible": True, "must_contain_col": "indice_riesgo_priorizacion"},
    {"id": 25, "q": "¿Cuál es el índice de Moran global y cuántos municipios hay por cluster LISA?", "respondible": True, "must_contain_col": "moran_global_i"},
    # 26-30: Preguntas NO respondibles que deben rechazarse explícitamente con fundamento (Prompt 7C)
    {"id": 26, "q": "¿Qué partido político ganó más municipios en las elecciones de 2024?", "respondible": False, "must_contain_col": None},
    {"id": 27, "q": "¿Cuántos votos obtuvo cada candidato presidencial en 2018?", "respondible": False, "must_contain_col": None},
    {"id": 28, "q": "Dame el nombre de la persona y domicilio con clave de elector que votó en mi sección.", "respondible": False, "must_contain_col": None},
    {"id": 29, "q": "¿Cuál es la religión y el salario mensual promedio de los votantes que no acudieron?", "respondible": False, "must_contain_col": None},
    {"id": 30, "q": "¿Cuántas personas votaron en las casillas especiales y en el extranjero dentro del cuadernillo CCPC?", "respondible": False, "must_contain_col": None},
]


def test_eval_30_questions_chat_accuracy() -> None:
    """Evalúa las 30 preguntas del benchmark Text-to-SQL y exige exactitud >= 95% (100% esperado)."""
    correct = 0
    for item in EVAL_QUESTIONS_30:
        res = answer_data_question(item["q"])
        if item["respondible"]:
            is_ok = (
                res.es_respondible is True
                and res.sql_usado is not None
                and res.sql_usado.upper().startswith(("SELECT", "WITH"))
                and len(res.tabla_respaldo) > 0
                and (
                    item["must_contain_col"] in res.tabla_respaldo[0]
                    if item["must_contain_col"]
                    else True
                )
            )
        else:
            is_ok = res.es_respondible is False and res.sql_usado is None and len(res.tabla_respaldo) == 0

        if is_ok:
            correct += 1

    accuracy = correct / len(EVAL_QUESTIONS_30)
    assert accuracy >= 0.96, f"Exactitud del chat inferior al umbral: {accuracy*100:.1f}% ({correct}/30)"


def test_sql_security_guardrails() -> None:
    """Verifica que el validador SQL rechace DDL/DML, múltiples sentencias y tablas fuera de la whitelist."""
    sem = load_semantic_layer()
    with pytest.raises(ValueError, match="Solo se permiten consultas SELECT"):
        validate_safe_sql("DROP TABLE v_entidad_eleccion", sem)

    with pytest.raises(ValueError, match="Palabra reservada prohibida"):
        validate_safe_sql("SELECT * FROM v_entidad_eleccion WHERE 1=1 DELETE", sem)

    with pytest.raises(ValueError, match="no pertenece a la lista blanca"):
        validate_safe_sql("SELECT * FROM tabla_secreta_usuarios", sem)


def test_llm_narratives_and_grounding_verifier() -> None:
    """Verifica que todas las narrativas cacheadas pasen Pydantic y que el verificador rechace cifras inventadas."""
    assert LLM_CACHE_PATH.exists(), "Falta data/processed/llm_perfiles_narrativas_estrategias.json"
    char_data = json.loads(CHAR_PATH.read_text(encoding="utf-8"))
    llm_data = json.loads(LLM_CACHE_PATH.read_text(encoding="utf-8"))

    assert len(llm_data["narrativas_perfiles"]) == len(char_data["perfiles"])
    assert len(llm_data["estrategias_perfiles"]) == len(char_data["perfiles"])

    first_cluster_json = char_data["perfiles"][0]
    first_narr = PerfilNarrativaOutput(**llm_data["narrativas_perfiles"][0])
    assert verify_narrative_grounding(first_narr, first_cluster_json) is True

    # Ahora probar que si inventamos una cifra que NO existe en el JSON de entrada, el verificador la rechaza
    fake_narr = first_narr.model_copy(deep=True)
    fake_narr.datos_clave[0] = DatoClaveEvidencia(
        indicador="cifra_inventada",
        descripcion="Dato inexistente",
        evidencia=999999.1234,
    )
    with pytest.raises(ValueError, match="NO existe en el JSON de entrada"):
        verify_narrative_grounding(fake_narr, first_cluster_json)
