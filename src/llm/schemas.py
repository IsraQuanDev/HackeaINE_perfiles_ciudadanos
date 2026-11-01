from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class DatoClaveEvidencia(BaseModel):
    indicador: str = Field(..., description="Nombre del campo o métrica en el JSON de caracterización")
    descripcion: str = Field(..., description="Oración descriptiva que contextualiza la cifra")
    evidencia: float | int = Field(..., description="Valor numérico exacto presente en el JSON de entrada")


class PerfilNarrativaOutput(BaseModel):
    cluster_id: int
    nombre: str = Field(..., description="Nombre del perfil (<= 4 palabras, no estigmatizante)")
    lema: str
    descripcion_narrativa: str = Field(..., description="Narrativa de 80 a 120 palabras")
    comunidad_ilustrativa: str = Field(
        ...,
        description="Descripción de comunidad/municipio ilustrativo marcada explícitamente como ejemplo ficticio",
    )
    datos_clave: list[DatoClaveEvidencia] = Field(..., min_length=3, max_length=3)
    tono_comunicacion: str

    @field_validator("nombre")
    @classmethod
    def validate_nombre_length_and_ethics(cls, v: str) -> str:
        words = v.strip().split()
        if len(words) > 4 or len(words) == 0:
            raise ValueError(f"El nombre del perfil debe tener entre 1 y 4 palabras (tiene {len(words)}): '{v}'")
        forbidden = {"apáticos", "apaticos", "ignorantes", "atrasados", "flojos", "desinteresados"}
        if any(w.lower() in forbidden for w in words):
            raise ValueError(f"El nombre contiene términos estigmatizantes prohibidos: '{v}'")
        return v.strip()

    @field_validator("descripcion_narrativa")
    @classmethod
    def validate_word_count_80_120(cls, v: str) -> str:
        words = v.strip().split()
        if not (80 <= len(words) <= 120):
            raise ValueError(
                f"La descripción narrativa debe tener entre 80 y 120 palabras (tiene {len(words)} palabras)"
            )
        return v.strip()

    @field_validator("comunidad_ilustrativa")
    @classmethod
    def validate_fictional_marker(cls, v: str) -> str:
        up = v.upper()
        if not any(tok in up for tok in ("DATO REAL", "PROTOTIPO", "FICTICIO", "ILUSTRATIVO")):
            raise ValueError(
                "comunidad_ilustrativa debe estar etiquetada explícitamente como DATO REAL (municipio prototipo) o ejemplo ilustrativo"
            )
        return v.strip()


class EstrategiaPerfilOutput(BaseModel):
    cluster_id: int
    nombre_perfil: str
    objetivo: str
    canales: list[str] = Field(..., min_length=2)
    mensaje_central: str
    aliados_institucionales: list[str] = Field(..., min_length=2)
    accion_concreta: str
    kpi_medible: str
    linea_base: float = Field(..., description="Línea base numérica tomada exactamente del JSON del perfil")
    unidad_kpi: str = Field(default="%")
    meta_2027: float
    riesgo_consideracion_etica: str
    fundamento_institucional_ine: str


class ChatSQLResponse(BaseModel):
    pregunta: str
    es_respondible: bool
    respuesta_natural: str
    sql_usado: str | None = None
    tabla_respaldo: list[dict[str, Any]] = Field(default_factory=list)
    tipo_grafica_sugerida: str = Field(default="table")
    fuente_trazable: str = Field(default="Catálogo DuckDB CCPC 2009-2024 (data/ccpc.duckdb)")


def extract_all_numbers_from_json(obj: Any) -> set[float]:
    """Extrae recursivamente todos los números presentes en el JSON de entrada de un perfil."""
    nums: set[float] = set()
    if isinstance(obj, bool):
        return nums
    if isinstance(obj, (int, float)):
        val = float(obj)
        nums.add(round(val, 6))
        nums.add(round(val, 4))
        nums.add(round(val, 2))
        nums.add(round(val * 100.0, 2))
        return nums
    if isinstance(obj, dict):
        for v in obj.values():
            # No incluir las claves de diccionarios salvo valores
            nums.update(extract_all_numbers_from_json(v))
    elif isinstance(obj, list):
        for item in obj:
            nums.update(extract_all_numbers_from_json(item))
    return nums


def verify_narrative_grounding(
    narrative: PerfilNarrativaOutput,
    cluster_input_json: dict[str, Any],
) -> bool:
    """
    Verificador automático (Prompt 7A):
    Toda cifra citada en `datos_clave[*].evidencia` debe existir en el JSON de entrada del cluster.
    Si alguna cifra no existe en el JSON de entrada, lanza ValueError para rechazar y reintentar.
    """
    allowed_numbers = extract_all_numbers_from_json(cluster_input_json)
    for item in narrative.datos_clave:
        ev = float(item.evidencia)
        matched = any(
            abs(ev - cand) <= 1e-4
            for cand in allowed_numbers
        )
        if not matched:
            raise ValueError(
                f"Cifra en evidencia ({item.evidencia} para '{item.indicador}') NO existe en el JSON de entrada del cluster {narrative.cluster_id}."
            )
    return True
