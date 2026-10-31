from __future__ import annotations

import urllib.request
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
EXTERNAL_DIR = BASE_DIR / "data" / "raw" / "external"

# URLs oficiales de Datos Abiertos de CONAPO (Índice de Marginación Municipal 2020) e INEGI (Censo 2020)
CONAPO_IMM_2020_URL = (
    "http://www.conapo.gob.mx/work/models/CONAPO/Marginacion/Datos_Abiertos/Municipio/IMM_2020.csv"
)


def fetch_or_load_external_enrichment(cve_geos: pd.Series) -> pd.DataFrame:
    """
    Intenta cargar o descargar los datos agregados municipales de INEGI Censo 2020 y CONAPO 2020.
    Cumpliendo estrictamente el Principio Inquebrantable #3 y el Prompt 2:
    - Si los archivos existen localmente en data/raw/external/, los carga y valida.
    - Si no existen, intenta descargarlos de la fuente pública oficial.
    - Si la red está restringida o el servidor externo no responde, NO inventa valores:
      genera el esquema esperado con valores nulos documentados y la bandera
      `flag_enriquecimiento_externo_stub = True`.
    """
    EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)
    local_csv = EXTERNAL_DIR / "enriquecimiento_inegi_conapo_2020.csv"

    if not local_csv.exists():
        try:
            req = urllib.request.Request(
                CONAPO_IMM_2020_URL,
                headers={"User-Agent": "Mozilla/5.0 (INE-Hackathon-Reproducible-Pipeline)"},
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                raw_bytes = resp.read()
            imm_raw_path = EXTERNAL_DIR / "IMM_2020_conapo.csv"
            imm_raw_path.write_bytes(raw_bytes)
            df_imm = pd.read_csv(imm_raw_path, encoding="latin1", low_memory=False)
            df_imm.columns = [c.strip().upper() for c in df_imm.columns]
            if "CVE_MUN" in df_imm.columns and "IM_2020" in df_imm.columns:
                out = pd.DataFrame()
                out["cve_geo"] = df_imm["CVE_MUN"].astype(int).map(lambda x: f"{x:05d}")
                out["conapo_indice_marginacion_2020"] = pd.to_numeric(
                    df_imm["IM_2020"], errors="coerce"
                )
                out["conapo_grado_marginacion_2020"] = (
                    df_imm["GM_2020"].astype(str) if "GM_2020" in df_imm.columns else pd.NA
                )
                # Variables de carencia educativa de CONAPO Censo 2020 (% población sin primaria completa / analfabetismo)
                out["conapo_pct_analfabetismo_2020"] = (
                    pd.to_numeric(df_imm["ANALF"], errors="coerce")
                    if "ANALF" in df_imm.columns
                    else float("nan")
                )
                out["conapo_pct_sin_educ_basica_2020"] = (
                    pd.to_numeric(df_imm["SBASC"], errors="coerce")
                    if "SBASC" in df_imm.columns
                    else float("nan")
                )
                out["inegi_grado_escolaridad_2020"] = float("nan")
                out["inegi_pct_viviendas_internet_2020"] = float("nan")
                out["flag_enriquecimiento_externo_stub"] = False
                out = out.drop_duplicates(subset=["cve_geo"])
                out.to_csv(local_csv, index=False, encoding="utf-8")
        except Exception as exc:
            print(
                f"[Enrichment] Aviso: No fue posible descargar datos externos en vivo ({exc}). "
                "Usando stub con esquema esperado y sin valores inventados (ver docs/fuentes.md)."
            )

    if local_csv.exists():
        df_ext = pd.read_csv(local_csv, dtype={"cve_geo": str})
        df_ext["cve_geo"] = df_ext["cve_geo"].str.zfill(5)
        base = pd.DataFrame({"cve_geo": cve_geos.astype(str).str.zfill(5).unique()})
        merged = base.merge(df_ext, on="cve_geo", how="left")
        if "flag_enriquecimiento_externo_stub" not in merged.columns:
            merged["flag_enriquecimiento_externo_stub"] = merged[
                "conapo_indice_marginacion_2020"
            ].isna()
        return merged

    # Stub transparente sin inventar un solo dato
    stub = pd.DataFrame({"cve_geo": cve_geos.astype(str).str.zfill(5).unique()})
    stub["conapo_indice_marginacion_2020"] = float("nan")
    stub["conapo_grado_marginacion_2020"] = pd.Series([None] * len(stub), dtype="object")
    stub["conapo_pct_analfabetismo_2020"] = float("nan")
    stub["conapo_pct_sin_educ_basica_2020"] = float("nan")
    stub["inegi_grado_escolaridad_2020"] = float("nan")
    stub["inegi_pct_viviendas_internet_2020"] = float("nan")
    stub["flag_enriquecimiento_externo_stub"] = True
    return stub
