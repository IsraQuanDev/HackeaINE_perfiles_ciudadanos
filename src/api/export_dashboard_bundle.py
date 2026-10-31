from __future__ import annotations

import json
import shutil
from pathlib import Path

import duckdb
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DUCKDB_PATH = BASE_DIR / "data" / "ccpc.duckdb"
APP_DATA_DIR = BASE_DIR / "app" / "public" / "data"


def export_dashboard_bundle() -> None:
    """
    Exporta todos los artefactos procesados y archivos Parquet hacia app/public/data/
    para que el frontend Next.js + DuckDB-WASM + MapLibre + ECharts cargue en < 1 segundo.
    """
    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Copiar archivos Parquet procesados para DuckDB-WASM local en el navegador
    for pq_name in [
        "features_municipio.parquet",
        "perfiles_municipio.parquet",
        "proyeccion_2027.parquet",
        "puente_municipio_anio.parquet",
        "ventanas_perfiles_municipio.parquet",
    ]:
        src = PROCESSED_DIR / pq_name
        if src.exists():
            shutil.copy2(src, APP_DATA_DIR / pq_name)

    # 2. Copiar JSONs estructurados
    for js_name in [
        "perfiles_caracterizacion.json",
        "transiciones.json",
        "simulador_what_if.json",
        "llm_perfiles_narrativas_estrategias.json",
        "clustering_model_metadata.json",
        "deep_learning_eval.json",
        "spatial_moran_summary.json",
    ]:
        src = PROCESSED_DIR / js_name
        if src.exists():
            shutil.copy2(src, APP_DATA_DIR / js_name)

    # 3. Construir el bundle maestro `dashboard_master.json` con GeoJSON ligero de puntos/polígonos municipales,
    # vistas por entidad y distrito, y buscador de municipios con sus vecinos espaciales más cercanos
    df_feat = pd.read_parquet(PROCESSED_DIR / "features_municipio.parquet")
    df_prof = pd.read_parquet(PROCESSED_DIR / "perfiles_municipio.parquet")
    df_proj = pd.read_parquet(PROCESSED_DIR / "proyeccion_2027.parquet")
    df_win = pd.read_parquet(PROCESSED_DIR / "ventanas_perfiles_municipio.parquet")

    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    ent_elec = con.execute("""
        SELECT anio, tipo_eleccion, modalidad, cve_ent, nom_ent, lista_nominal, votantes,
               ROUND(participacion * 100, 2) AS participacion_pct
        FROM v_entidad_eleccion
        ORDER BY anio, cve_ent, modalidad
    """).df()
    dist_elec = con.execute("""
        SELECT anio, tipo_eleccion, cve_ent, nom_ent, def, lista_nominal, votantes,
               ROUND(participacion * 100, 2) AS participacion_pct
        FROM v_distrito_eleccion
        WHERE modalidad = 'presencial'
        ORDER BY anio, cve_ent, def
    """).df()
    con.close()

    merged = (
        df_feat.merge(
            df_prof[["cve_geo", "cluster_id", "probabilidad_pertenencia", "distancia_centroide", "pca_1", "pca_2", "umap_1", "umap_2"]],
            on="cve_geo",
        )
        .merge(
            df_proj[
                [
                    "cve_geo",
                    "ln_proyectada_2027",
                    "proyeccion_part_2027",
                    "intervalo_80_inf",
                    "intervalo_80_sup",
                    "votantes_esperados_2027",
                    "es_zona_riesgo_2027",
                    "indice_riesgo_priorizacion",
                ]
            ],
            on="cve_geo",
        )
        .merge(
            df_win[["cve_geo", "2009-2015", "2012-2018", "2015-2021", "2018-2024", "cambio_perfil_extremos"]],
            on="cve_geo",
        )
    )

    municipios_records = []
    for _, r in merged.iterrows():
        municipios_records.append(
            {
                "cve_geo": str(r["cve_geo"]),
                "cve_ent": str(r["cve_ent"]),
                "nom_ent": str(r["nom_ent"]),
                "cve_mun": str(r["cve_mun"]),
                "nom_mun": str(r["nom_mun"]),
                "def": str(r.get("def_principal", "1")),
                "cluster_id": int(r["cluster_id"]),
                "prob": round(float(r["probabilidad_pertenencia"]), 3),
                "lat": round(float(r["lat_aprox"]), 4),
                "lon": round(float(r["lon_aprox"]), 4),
                "p2009": round(float(r["part_2009"]) * 100, 2),
                "p2012": round(float(r["part_2012"]) * 100, 2),
                "p2015": round(float(r["part_2015"]) * 100, 2),
                "p2018": round(float(r["part_2018"]) * 100, 2),
                "p2021": round(float(r["part_2021"]) * 100, 2),
                "p2024": round(float(r["part_2024"]) * 100, 2),
                "p_global": round(float(r["part_media_global"]) * 100, 2),
                "p_pres": round(float(r["part_media_presidencial"]) * 100, 2),
                "p_inter": round(float(r["part_media_intermedia"]) * 100, 2),
                "caida_pi": round(float(r["caida_presidencial_intermedia"]) * 100, 2),
                "pendiente": round(float(r["pendiente_tendencia"]) * 100, 2),
                "volatilidad": round(float(r["volatilidad"]) * 100, 2),
                "constancia": round(float(r["constancia_sobre_mediana"]) * 100, 1),
                "brecha_gen": round(float(r["brecha_genero_media"]) * 100, 2),
                "brecha_edad": round(float(r["brecha_generacional_60_vs_18_29"]) * 100, 2),
                "p_joven": round(float(r["part_media_jovenes_18_29"]) * 100, 2),
                "p_60mas": round(float(r["part_media_adultos_60_mas"]) * 100, 2),
                "rural_pct": round(float(r["pct_ln_rural"]) * 100, 1),
                "urbana_pct": round(float(r["pct_ln_urbana"]) * 100, 1),
                "ln_2024": int(r["ln_2024"]),
                "va_2024": int(r["votantes_anticipado_2024"]),
                "va_tasa_10k": round(float(r["tasa_voto_anticipado_por_10k"]), 2),
                "baja_conf": bool(r["flag_baja_confiabilidad"]),
                "lisa": str(r["lisa_cluster"]),
                "w_09_15": int(r["2009-2015"]),
                "w_12_18": int(r["2012-2018"]),
                "w_15_21": int(r["2015-2021"]),
                "w_18_24": int(r["2018-2024"]),
                "cambio_w": bool(r["cambio_perfil_extremos"]),
                "ln_2027": int(r["ln_proyectada_2027"]),
                "p2027": round(float(r["proyeccion_part_2027"]) * 100, 2),
                "p2027_lo": round(float(r["intervalo_80_inf"]) * 100, 2),
                "p2027_hi": round(float(r["intervalo_80_sup"]) * 100, 2),
                "riesgo_2027": bool(r["es_zona_riesgo_2027"]),
                "idx_riesgo": int(r["indice_riesgo_priorizacion"]),
            }
        )

    ent_records = json.loads(ent_elec.to_json(orient="records"))
    dist_records = json.loads(dist_elec[dist_elec["anio"] == 2024].to_json(orient="records"))

    master_payload = {
        "municipios": municipios_records,
        "vista_entidades": ent_records,
        "vista_distritos_2024": dist_records,
    }

    (APP_DATA_DIR / "municipios_bundle.json").write_text(
        json.dumps(master_payload, ensure_ascii=False, allow_nan=False), encoding="utf-8"
    )
    print(f"[Export] Bundle para Dashboard exportado en {APP_DATA_DIR} ({len(municipios_records):,} municipios).")


if __name__ == "__main__":
    export_dashboard_bundle()
