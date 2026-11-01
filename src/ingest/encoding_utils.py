from __future__ import annotations

import unicodedata
from pathlib import Path

ENTIDADES_OFICIALES_UTF8: dict[int, str] = {
    1: "Aguascalientes",
    2: "Baja California",
    3: "Baja California Sur",
    4: "Campeche",
    5: "Coahuila",
    6: "Colima",
    7: "Chiapas",
    8: "Chihuahua",
    9: "Ciudad de México",
    10: "Durango",
    11: "Guanajuato",
    12: "Guerrero",
    13: "Hidalgo",
    14: "Jalisco",
    15: "Estado de México",
    16: "Michoacán",
    17: "Morelos",
    18: "Nayarit",
    19: "Nuevo León",
    20: "Oaxaca",
    21: "Puebla",
    22: "Querétaro",
    23: "Quintana Roo",
    24: "San Luis Potosí",
    25: "Sinaloa",
    26: "Sonora",
    27: "Tabasco",
    28: "Tamaulipas",
    29: "Tlaxcala",
    30: "Veracruz",
    31: "Yucatán",
    32: "Zacatecas",
}


def detect_file_encoding(fpath: str | Path, sample_bytes: int = 131072) -> str:
    """
    Detecta la codificación real de un archivo CSV/TXT leyendo una muestra de bytes.
    Prioriza UTF-8 (con o sin BOM) y cae en latin1/cp1252 si existen bytes no válidos en UTF-8.
    """
    path = Path(fpath)
    with path.open("rb") as f:
        raw = f.read(sample_bytes)
    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf8"
    try:
        raw.decode("utf-8")
        return "utf8"
    except UnicodeDecodeError:
        return "latin1"


def fix_mojibake_utf8_nfc(text: str | None) -> str:
    """
    Repara cadenas que sufrieron doble decodificación (UTF-8 leído como Latin-1/CP1252,
    produciendo patrones como 'GÃ³mez FarÃas', 'QuerÃ©taro', 'LeÃ³n') y normaliza a Unicode NFC.
    """
    if text is None:
        return ""
    s = str(text).strip()
    if not s:
        return ""

    # Remover posibles restos de BOM al inicio
    for bom_prefix in ("\ufeff", "ï»¿", "Ï»¿"):
        if s.startswith(bom_prefix):
            s = s[len(bom_prefix) :].strip()

    # Si contiene marcadores clásicos de mojibake UTF-8 -> Latin-1 ('Ã' o 'Â')
    if "Ã" in s or "Â" in s:
        try:
            repaired = s.encode("latin1").decode("utf-8")
            s = repaired
        except (UnicodeEncodeError, UnicodeDecodeError):
            # Reparación por reemplazo de secuencias comunes cuando algún byte fue alterado por CP1252
            replacements = {
                "Ã¡": "á",
                "Ã©": "é",
                "Ã­": "í",
                "Ã³": "ó",
                "Ãº": "ú",
                "Ã±": "ñ",
                "Ã¼": "ü",
                "Ã\x81": "Á",
                "Ã\x89": "É",
                "Ã\x8d": "Í",
                "Ã\x93": "Ó",
                "Ã\x9a": "Ú",
                "Ã\x91": "Ñ",
                "Ã\x9c": "Ü",
                "FarÃas": "Farías",
                "MarÃa": "María",
                "RÃo": "Río",
                "DÃaz": "Díaz",
                "MartÃnez": "Martínez",
                "GarcÃa": "García",
                "Â": "",
            }
            for bad, good in replacements.items():
                s = s.replace(bad, good)
            # Si aún queda 'Ã' aislada antes de consonante (caso 0xC3 0xAD donde 0xAD soft-hyphen se omitió)
            if "Ã" in s:
                s = s.replace("Ã", "í")

    return unicodedata.normalize("NFC", s)
