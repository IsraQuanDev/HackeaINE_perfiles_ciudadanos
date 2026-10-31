from __future__ import annotations

import glob
import os
import time
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd
import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
INTERIM_DIR = BASE_DIR / "data" / "interim"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DOCS_DIR = BASE_DIR / "docs"
DUCKDB_PATH = BASE_DIR / "data" / "ccpc.duckdb"

ENTIDADES_OFICIALES: dict[int, str] = {
    1: "AGUASCALIENTES",
    2: "BAJA CALIFORNIA",
    3: "BAJA CALIFORNIA SUR",
    4: "CAMPECHE",
    5: "COAHUILA",
    6: "COLIMA",
    7: "CHIAPAS",
    8: "CHIHUAHUA",
    9: "CIUDAD DE MEXICO",
    10: "DURANGO",
    11: "GUANAJUATO",
    12: "GUERRERO",
    13: "HIDALGO",
    14: "JALISCO",
    15: "ESTADO DE MEXICO",
    16: "MICHOACAN",
    17: "MORELOS",
    18: "NAYARIT",
    19: "NUEVO LEON",
    20: "OAXACA",
    21: "PUEBLA",
    22: "QUERETARO",
    23: "QUINTANA ROO",
    24: "SAN LUIS POTOSI",
    25: "SINALOA",
    26: "SONORA",
    27: "TABASCO",
    28: "TAMAULIPAS",
    29: "TLAXCALA",
    30: "VERACRUZ",
    31: "YUCATAN",
    32: "ZACATECAS",
}

ORDINARY_YEARS = [2009, 2012, 2015, 2018, 2021, 2024]
PRESIDENTIAL_YEARS = {2012, 2018, 2024}


def _find_dataset_folder(folder_name: str) -> Path:
    """Busca la carpeta en data/raw o en la raíz del proyecto."""
    candidate_raw = RAW_DIR / folder_name
    if candidate_raw.exists():
        return candidate_raw
    candidate_root = BASE_DIR / folder_name
    if candidate_root.exists():
        return candidate_root
    raise FileNotFoundError(f"No se encontró el directorio de datos: {folder_name}")


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [
        str(c).lstrip("\ufeff").lstrip("ï»¿").lstrip("Ï»¿").strip().upper()
        for c in df.columns
    ]
    return df


def _map_sexo(series: pd.Series) -> pd.Series:
    return series.map({0: "H", 1: "M", 2: "NB"}).fillna("NE")


def _map_rango_edad(series: pd.Series) -> pd.Series:
    # 18-29 (jóvenes), 30-59 (adultos), 60+ (adultos mayores)
    bins = [0, 29, 59, 200]
    labels = ["18-29", "30-59", "60+"]
    return pd.cut(series, bins=bins, labels=labels, right=True).astype(str)


def process_ordinary_year(year: int) -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, Any]]:
    """Procesa los 32 CSV de un año de conteo censal ordinario."""
    folder = _find_dataset_folder(f"DatosAbiertos_DECEyEC_ConteosCensales{year}")
    csv_files = sorted(glob.glob(str(folder / "**" / "*.csv"), recursive=True))
    if len(csv_files) != 32:
        raise RuntimeError(f"Se esperaban 32 archivos CSV para {year}, encontrados: {len(csv_files)}")

    tipo_eleccion = "presidencial" if year in PRESIDENTIAL_YEARS else "intermedia"
    year_chunks: list[pd.DataFrame] = []
    control_rows: list[dict[str, Any]] = []

    quality_stats = {
        "anio": year,
        "raw_rows": 0,
        "nulls_del": 0,
        "nulls_def": 0,
        "edad_gt_100_rows": 0,
        "edad_gt_100_ln": 0,
        "ns_gt_0_rows": 0,
        "ns_total": 0,
        "part_gt_100_rows": 0,
        "part_lt_0_rows": 0,
        "mismatch_ln_sv_nv_ns": 0,
    }

    for fpath in csv_files:
        pl_df = pl.read_csv(
            fpath,
            encoding="latin1",
            infer_schema_length=10000,
            ignore_errors=False,
        )
        rename_map = {
            c: str(c).lstrip("\ufeff").lstrip("ï»¿").lstrip("Ï»¿").strip().upper()
            for c in pl_df.columns
        }
        pl_df = pl_df.rename(rename_map)

        n_rows = pl_df.height
        quality_stats["raw_rows"] += n_rows
        quality_stats["nulls_del"] += int(pl_df["DEL"].null_count())
        quality_stats["nulls_def"] += int(pl_df["DEF"].null_count())

        edad_gt_100_df = pl_df.filter(pl.col("EDAD") > 100)
        quality_stats["edad_gt_100_rows"] += int(edad_gt_100_df.height)
        quality_stats["edad_gt_100_ln"] += int(edad_gt_100_df["LN"].sum() or 0)

        quality_stats["ns_gt_0_rows"] += int(pl_df.filter(pl.col("NS") > 0).height)
        quality_stats["ns_total"] += int(pl_df["NS"].sum() or 0)

        quality_stats["part_gt_100_rows"] += int(pl_df.filter(pl.col("SV") > pl.col("LN")).height)
        quality_stats["part_lt_0_rows"] += int(
            pl_df.filter((pl.col("SV") < 0) | (pl.col("LN") < 0)).height
        )
        quality_stats["mismatch_ln_sv_nv_ns"] += int(
            pl_df.filter(pl.col("LN") != (pl.col("SV") + pl.col("NV") + pl.col("NS"))).height
        )

        edo_int = int(pl_df["EDOCVE"][0])
        cve_ent_val = f"{edo_int:02d}"
        nom_ent_val = ENTIDADES_OFICIALES[edo_int]

        control_rows.append(
            {
                "anio": year,
                "modalidad": "presencial",
                "archivo": os.path.basename(fpath),
                "cve_ent": cve_ent_val,
                "nom_ent": nom_ent_val,
                "raw_rows": n_rows,
                "ln_fuente": int(pl_df["LN"].sum()),
                "sv_fuente": int(pl_df["SV"].sum()),
                "nv_fuente": int(pl_df["NV"].sum()),
                "ns_fuente": int(pl_df["NS"].sum()),
            }
        )

        grouped_pl = (
            pl_df.with_columns(
                [
                    pl.lit(cve_ent_val).alias("cve_ent"),
                    pl.lit(nom_ent_val).alias("nom_ent"),
                    pl.col("MPIOCVE").cast(pl.Int64).cast(pl.Utf8).str.zfill(3).alias("cve_mun"),
                    pl.col("MPIONOM").cast(pl.Utf8).str.strip_chars().alias("nom_mun"),
                    pl.col("DEF")
                    .cast(pl.Utf8)
                    .fill_null("SN")
                    .str.replace(r"\.0$", "")
                    .str.strip_chars()
                    .alias("def"),
                    pl.col("DEL")
                    .cast(pl.Utf8)
                    .fill_null("SN")
                    .str.replace(r"\.0$", "")
                    .str.strip_chars()
                    .alias("del"),
                    pl.col("TIPOSEC")
                    .cast(pl.Utf8)
                    .fill_null("NA")
                    .str.strip_chars()
                    .str.to_uppercase()
                    .alias("tiposec"),
                    pl.when(pl.col("SEXO") == 0)
                    .then(pl.lit("H"))
                    .when(pl.col("SEXO") == 1)
                    .then(pl.lit("M"))
                    .when(pl.col("SEXO") == 2)
                    .then(pl.lit("NB"))
                    .otherwise(pl.lit("NE"))
                    .alias("sexo"),
                    pl.when(pl.col("EDAD") <= 29)
                    .then(pl.lit("18-29"))
                    .when(pl.col("EDAD") <= 59)
                    .then(pl.lit("30-59"))
                    .otherwise(pl.lit("60+"))
                    .alias("rango_edad"),
                ]
            )
            .with_columns((pl.col("cve_ent") + pl.col("cve_mun")).alias("cve_geo"))
            .group_by(
                [
                    "cve_ent",
                    "nom_ent",
                    "cve_mun",
                    "cve_geo",
                    "def",
                    "del",
                    "tiposec",
                    "sexo",
                    "rango_edad",
                ],
                maintain_order=True,
            )
            .agg(
                [
                    pl.col("nom_mun").first().alias("nom_mun"),
                    pl.col("LN").sum().alias("lista_nominal"),
                    pl.col("SV").sum().alias("votantes"),
                    pl.col("NV").sum().alias("no_votantes"),
                    pl.col("NS").sum().alias("no_especificados"),
                ]
            )
        )

        grouped = grouped_pl.to_pandas()
        grouped["anio"] = year
        grouped["tipo_eleccion"] = tipo_eleccion
        grouped["modalidad"] = "presencial"
        grouped["participacion"] = grouped["votantes"] / grouped["lista_nominal"].replace(0, pd.NA)
        grouped["participacion"] = grouped["participacion"].astype(float)
        grouped["celda_pequena_lt10"] = grouped["lista_nominal"] < 10

        year_chunks.append(grouped)

    df_year = pd.concat(year_chunks, ignore_index=True)
    cols_order = [
        "anio",
        "tipo_eleccion",
        "modalidad",
        "cve_ent",
        "nom_ent",
        "cve_mun",
        "cve_geo",
        "nom_mun",
        "def",
        "del",
        "tiposec",
        "sexo",
        "rango_edad",
        "lista_nominal",
        "votantes",
        "no_votantes",
        "no_especificados",
        "participacion",
        "celda_pequena_lt10",
    ]
    return df_year[cols_order], control_rows, quality_stats


def process_special_2024() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    """Procesa Voto Anticipado 2024 y Prisión Preventiva 2024."""
    chunks: list[pd.DataFrame] = []
    control_rows: list[dict[str, Any]] = []

    # 1. Voto Anticipado 2024
    va_folder = _find_dataset_folder("DatosAbiertos_DECEyEC_ConteosCensales_VotoAnticipado2024")
    va_csvs = sorted(glob.glob(str(va_folder / "**" / "*.csv"), recursive=True))
    if not va_csvs:
        raise FileNotFoundError("No se encontró el CSV de Voto Anticipado 2024")
    df_va = pd.read_csv(va_csvs[0], encoding="latin1", low_memory=False)
    df_va = _clean_columns(df_va)
    df_va["cve_ent"] = df_va["EDOCVE"].astype(int).map(lambda x: f"{x:02d}")
    df_va["nom_ent"] = df_va["EDOCVE"].astype(int).map(ENTIDADES_OFICIALES)
    df_va["cve_mun"] = df_va["MPIOCVE"].astype(int).map(lambda x: f"{x:03d}")
    df_va["cve_geo"] = df_va["cve_ent"] + df_va["cve_mun"]
    df_va["nom_mun"] = df_va["MPIONOM"].astype(str).str.strip()
    df_va["def"] = df_va["DEF"].astype(str).str.strip()
    df_va["del"] = df_va["DEL"].astype(str).str.strip()
    df_va["tiposec"] = "NA"
    df_va["sexo"] = _map_sexo(df_va["SEXO"])
    df_va["rango_edad"] = "NO_ESPECIFICADO"

    for edo_int, grp in df_va.groupby(df_va["EDOCVE"].astype(int)):
        control_rows.append(
            {
                "anio": 2024,
                "modalidad": "anticipado",
                "archivo": os.path.basename(va_csvs[0]),
                "cve_ent": f"{edo_int:02d}",
                "nom_ent": ENTIDADES_OFICIALES[edo_int],
                "raw_rows": len(grp),
                "ln_fuente": 0,
                "sv_fuente": len(grp),
                "nv_fuente": 0,
                "ns_fuente": 0,
            }
        )

    va_grouped = (
        df_va.groupby(
            ["cve_ent", "nom_ent", "cve_mun", "cve_geo", "def", "del", "tiposec", "sexo", "rango_edad"],
            as_index=False,
        )
        .agg(
            nom_mun=("nom_mun", "first"),
            votantes=("cve_ent", "count"),
        )
    )
    va_grouped["anio"] = 2024
    va_grouped["tipo_eleccion"] = "presidencial"
    va_grouped["modalidad"] = "anticipado"
    va_grouped["lista_nominal"] = 0
    va_grouped["no_votantes"] = 0
    va_grouped["no_especificados"] = 0
    va_grouped["participacion"] = float("nan")
    va_grouped["celda_pequena_lt10"] = va_grouped["votantes"] < 10
    chunks.append(va_grouped)

    # 2. Prisión Preventiva 2024 (sin municipio: cve_mun = '000')
    pp_folder = _find_dataset_folder("DatosAbiertos_DECEyEC_ConteosCensales_PrisionPreventiva2024")
    pp_csvs = sorted(glob.glob(str(pp_folder / "**" / "*.csv"), recursive=True))
    if not pp_csvs:
        raise FileNotFoundError("No se encontró el CSV de Prisión Preventiva 2024")
    df_pp = pd.read_csv(pp_csvs[0], encoding="latin1", low_memory=False)
    df_pp = _clean_columns(df_pp)
    df_pp["cve_ent"] = df_pp["ESTADO"].astype(int).map(lambda x: f"{x:02d}")
    df_pp["nom_ent"] = df_pp["ESTADO"].astype(int).map(ENTIDADES_OFICIALES)
    df_pp["cve_mun"] = "000"
    df_pp["cve_geo"] = df_pp["cve_ent"] + "000"
    df_pp["nom_mun"] = "SIN_MUNICIPIO_PRISION_PREVENTIVA"
    df_pp["def"] = df_pp["DEF"].astype(str).str.strip()
    df_pp["del"] = "SN"
    df_pp["tiposec"] = "NA"
    df_pp["sexo"] = _map_sexo(df_pp["SEXO"])
    df_pp["rango_edad"] = "NO_ESPECIFICADO"

    for edo_int, grp in df_pp.groupby(df_pp["ESTADO"].astype(int)):
        control_rows.append(
            {
                "anio": 2024,
                "modalidad": "prision_preventiva",
                "archivo": os.path.basename(pp_csvs[0]),
                "cve_ent": f"{edo_int:02d}",
                "nom_ent": ENTIDADES_OFICIALES[edo_int],
                "raw_rows": len(grp),
                "ln_fuente": 0,
                "sv_fuente": len(grp),
                "nv_fuente": 0,
                "ns_fuente": 0,
            }
        )

    pp_grouped = (
        df_pp.groupby(
            ["cve_ent", "nom_ent", "cve_mun", "cve_geo", "nom_mun", "def", "del", "tiposec", "sexo", "rango_edad"],
            as_index=False,
        )
        .agg(votantes=("cve_ent", "count"))
    )
    pp_grouped["anio"] = 2024
    pp_grouped["tipo_eleccion"] = "presidencial"
    pp_grouped["modalidad"] = "prision_preventiva"
    pp_grouped["lista_nominal"] = 0
    pp_grouped["no_votantes"] = 0
    pp_grouped["no_especificados"] = 0
    pp_grouped["participacion"] = float("nan")
    pp_grouped["celda_pequena_lt10"] = pp_grouped["votantes"] < 10
    chunks.append(pp_grouped)

    cols_order = [
        "anio",
        "tipo_eleccion",
        "modalidad",
        "cve_ent",
        "nom_ent",
        "cve_mun",
        "cve_geo",
        "nom_mun",
        "def",
        "del",
        "tiposec",
        "sexo",
        "rango_edad",
        "lista_nominal",
        "votantes",
        "no_votantes",
        "no_especificados",
        "participacion",
        "celda_pequena_lt10",
    ]
    df_special = pd.concat([c[cols_order] for c in chunks], ignore_index=True)
    return df_special, control_rows


def build_geographic_bridge(df_all: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla puente municipio-año para manejar creación/fusión de municipios (2009-2024)."""
    df_pres = df_all[df_all["modalidad"] == "presencial"].copy()
    mun_year = (
        df_pres.groupby(["cve_geo", "cve_ent", "nom_ent", "cve_mun", "anio"], as_index=False)
        .agg(
            nom_mun=("nom_mun", "first"),
            lista_nominal=("lista_nominal", "sum"),
            votantes=("votantes", "sum"),
            n_distritos_fed=("def", "nunique"),
        )
    )

    bridge = (
        mun_year.sort_values(["cve_geo", "anio"])
        .groupby(["cve_geo", "cve_ent", "nom_ent", "cve_mun"], as_index=False)
        .agg(
            nom_mun=("nom_mun", "last"),
            n_elecciones_presente=("anio", "nunique"),
            primer_anio=("anio", "min"),
            ultimo_anio=("anio", "max"),
            anios_presente=("anio", lambda s: ",".join(str(x) for x in sorted(s.unique()))),
            ln_promedio=("lista_nominal", "mean"),
            ln_ultimo_anio=("lista_nominal", "last"),
        )
    )
    bridge["es_panel_completo"] = bridge["n_elecciones_presente"] == len(ORDINARY_YEARS)

    def _classify_change(row: pd.Series) -> str:
        if row["es_panel_completo"]:
            return "ESTABLE_2009_2024"
        if row["primer_anio"] > 2009 and row["ultimo_anio"] == 2024:
            return f"NUEVA_CREACION_{row['primer_anio']}"
        if row["ultimo_anio"] < 2024:
            return f"SIN_REGISTRO_POST_{row['ultimo_anio']}"
        return "INTERMITENTE_O_CASO_ESPECIAL"

    bridge["estatus_marco_geografico"] = bridge.apply(_classify_change, axis=1)
    return bridge.sort_values("cve_geo").reset_index(drop=True)


def create_duckdb_catalog(
    parquet_dir: Path,
    bridge_path: Path,
    control_path: Path,
    duckdb_path: Path,
) -> None:
    """Crea el catálogo DuckDB con vistas por municipio, distrito y entidad."""
    if duckdb_path.exists():
        duckdb_path.unlink()

    con = duckdb.connect(str(duckdb_path))
    p_glob = str(parquet_dir / "**" / "*.parquet").replace("\\", "/")
    b_path = str(bridge_path).replace("\\", "/")
    c_path = str(control_path).replace("\\", "/")

    con.execute(f"""
        CREATE VIEW ccpc_unificado AS
        SELECT * FROM read_parquet('{p_glob}', hive_partitioning=true);
    """)

    con.execute(f"""
        CREATE TABLE puente_municipio_anio AS
        SELECT * FROM read_parquet('{b_path}');
    """)

    con.execute(f"""
        CREATE TABLE control_totales_fuente AS
        SELECT * FROM read_parquet('{c_path}');
    """)

    # Vista por Municipio y Elección (incluyendo desgloses de sexo, edad, tipo de sección y voto anticipado)
    con.execute("""
        CREATE VIEW v_municipio_eleccion AS
        WITH base_pres AS (
            SELECT
                anio,
                tipo_eleccion,
                cve_ent,
                nom_ent,
                cve_mun,
                cve_geo,
                FIRST(nom_mun) AS nom_mun,
                SUM(lista_nominal) AS lista_nominal,
                SUM(votantes) AS votantes,
                SUM(no_votantes) AS no_votantes,
                SUM(no_especificados) AS no_especificados,
                SUM(votantes)::DOUBLE / NULLIF(SUM(lista_nominal), 0) AS participacion,
                -- Desglose por sexo (suprimiendo tasas si LN < 10 por regla de privacidad #1)
                SUM(CASE WHEN sexo = 'M' THEN lista_nominal ELSE 0 END) AS ln_mujeres,
                SUM(CASE WHEN sexo = 'M' THEN votantes ELSE 0 END) AS votantes_mujeres,
                CASE
                    WHEN SUM(CASE WHEN sexo = 'M' THEN lista_nominal ELSE 0 END) >= 10
                    THEN SUM(CASE WHEN sexo = 'M' THEN votantes ELSE 0 END)::DOUBLE
                         / SUM(CASE WHEN sexo = 'M' THEN lista_nominal ELSE 0 END)
                    ELSE NULL
                END AS part_mujeres,
                SUM(CASE WHEN sexo = 'H' THEN lista_nominal ELSE 0 END) AS ln_hombres,
                SUM(CASE WHEN sexo = 'H' THEN votantes ELSE 0 END) AS votantes_hombres,
                CASE
                    WHEN SUM(CASE WHEN sexo = 'H' THEN lista_nominal ELSE 0 END) >= 10
                    THEN SUM(CASE WHEN sexo = 'H' THEN votantes ELSE 0 END)::DOUBLE
                         / SUM(CASE WHEN sexo = 'H' THEN lista_nominal ELSE 0 END)
                    ELSE NULL
                END AS part_hombres,
                -- Desglose por edad (18-29, 30-59, 60+)
                SUM(CASE WHEN rango_edad = '18-29' THEN lista_nominal ELSE 0 END) AS ln_18_29,
                SUM(CASE WHEN rango_edad = '18-29' THEN votantes ELSE 0 END) AS vot_18_29,
                CASE
                    WHEN SUM(CASE WHEN rango_edad = '18-29' THEN lista_nominal ELSE 0 END) >= 10
                    THEN SUM(CASE WHEN rango_edad = '18-29' THEN votantes ELSE 0 END)::DOUBLE
                         / SUM(CASE WHEN rango_edad = '18-29' THEN lista_nominal ELSE 0 END)
                    ELSE NULL
                END AS part_18_29,
                SUM(CASE WHEN rango_edad = '30-59' THEN lista_nominal ELSE 0 END) AS ln_30_59,
                SUM(CASE WHEN rango_edad = '30-59' THEN votantes ELSE 0 END) AS vot_30_59,
                CASE
                    WHEN SUM(CASE WHEN rango_edad = '30-59' THEN lista_nominal ELSE 0 END) >= 10
                    THEN SUM(CASE WHEN rango_edad = '30-59' THEN votantes ELSE 0 END)::DOUBLE
                         / SUM(CASE WHEN rango_edad = '30-59' THEN lista_nominal ELSE 0 END)
                    ELSE NULL
                END AS part_30_59,
                SUM(CASE WHEN rango_edad = '60+' THEN lista_nominal ELSE 0 END) AS ln_60_mas,
                SUM(CASE WHEN rango_edad = '60+' THEN votantes ELSE 0 END) AS vot_60_mas,
                CASE
                    WHEN SUM(CASE WHEN rango_edad = '60+' THEN lista_nominal ELSE 0 END) >= 10
                    THEN SUM(CASE WHEN rango_edad = '60+' THEN votantes ELSE 0 END)::DOUBLE
                         / SUM(CASE WHEN rango_edad = '60+' THEN lista_nominal ELSE 0 END)
                    ELSE NULL
                END AS part_60_mas,
                -- Desglose por tipo de sección (Urbana, Mixta, Rural)
                SUM(CASE WHEN tiposec = 'U' THEN lista_nominal ELSE 0 END) AS ln_urbana,
                SUM(CASE WHEN tiposec = 'M' THEN lista_nominal ELSE 0 END) AS ln_mixta,
                SUM(CASE WHEN tiposec = 'R' THEN lista_nominal ELSE 0 END) AS ln_rural,
                SUM(lista_nominal) < 10 AS suprimido_privacidad_lt10
            FROM ccpc_unificado
            WHERE modalidad = 'presencial'
            GROUP BY anio, tipo_eleccion, cve_ent, nom_ent, cve_mun, cve_geo
        ),
        voto_ant AS (
            SELECT
                anio,
                cve_geo,
                SUM(votantes) AS votantes_anticipado
            FROM ccpc_unificado
            WHERE modalidad = 'anticipado'
            GROUP BY anio, cve_geo
        )
        SELECT
            b.*,
            COALESCE(va.votantes_anticipado, 0) AS votantes_anticipado
        FROM base_pres b
        LEFT JOIN voto_ant va
          ON b.anio = va.anio AND b.cve_geo = va.cve_geo;
    """)

    # Vista por Distrito Electoral Federal y Elección
    con.execute("""
        CREATE VIEW v_distrito_eleccion AS
        SELECT
            anio,
            tipo_eleccion,
            modalidad,
            cve_ent,
            nom_ent,
            def,
            SUM(lista_nominal) AS lista_nominal,
            SUM(votantes) AS votantes,
            SUM(no_votantes) AS no_votantes,
            SUM(no_especificados) AS no_especificados,
            CASE
                WHEN SUM(lista_nominal) >= 10
                THEN SUM(votantes)::DOUBLE / SUM(lista_nominal)
                ELSE NULL
            END AS participacion,
            (SUM(lista_nominal) > 0 AND SUM(lista_nominal) < 10)
                OR (SUM(lista_nominal) = 0 AND SUM(votantes) < 10) AS suprimido_privacidad_lt10
        FROM ccpc_unificado
        GROUP BY anio, tipo_eleccion, modalidad, cve_ent, nom_ent, def;
    """)

    # Vista por Entidad Federativa y Elección
    con.execute("""
        CREATE VIEW v_entidad_eleccion AS
        SELECT
            anio,
            tipo_eleccion,
            modalidad,
            cve_ent,
            nom_ent,
            SUM(lista_nominal) AS lista_nominal,
            SUM(votantes) AS votantes,
            SUM(no_votantes) AS no_votantes,
            SUM(no_especificados) AS no_especificados,
            CASE
                WHEN SUM(lista_nominal) >= 10
                THEN SUM(votantes)::DOUBLE / SUM(lista_nominal)
                ELSE NULL
            END AS participacion
        FROM ccpc_unificado
        GROUP BY anio, tipo_eleccion, modalidad, cve_ent, nom_ent;
    """)

    con.close()


def write_quality_report(
    quality_list: list[dict[str, Any]],
    bridge_df: pd.DataFrame,
    control_df: pd.DataFrame,
) -> None:
    """Genera el reporte de calidad de datos en docs/calidad_datos.md."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    q_df = pd.DataFrame(quality_list)

    status_counts = bridge_df["estatus_marco_geografico"].value_index if hasattr(bridge_df["estatus_marco_geografico"], "value_index") else bridge_df["estatus_marco_geografico"].value_counts()

    lines = [
        "# Reporte de Calidad de Datos e Integridad de Ingesta (CCPC 2009–2024)",
        "",
        "## 1. Resumen de Validación y Conciliación de Totales",
        "",
        f"- **Archivos procesados:** {len(control_df[control_df['modalidad']=='presencial'])} archivos CSV ordinarios (32 entidades × 6 elecciones) + 2 archivos nacionales de modalidades especiales 2024 (`VotoAnticipado2024` y `PrisionPreventiva2024`).",
        f"- **Filas crudas totales inspeccionadas (presencial):** {int(q_df['raw_rows'].sum()):,}",
        f"- **Celdas con participación > 100% (`SV > LN`):** {int(q_df['part_gt_100_rows'].sum()):,}",
        f"- **Celdas con participación < 0% (`SV < 0` o `LN < 0`):** {int(q_df['part_lt_0_rows'].sum()):,}",
        f"- **Celdas donde `LN != SV + NV + NS`:** {int(q_df['mismatch_ln_sv_nv_ns'].sum()):,}",
        "",
        "## 2. Métricas de Calidad por Año Electoral (Modalidad Presencial)",
        "",
        "| Año | Filas Crudas | Nulos en `DEF` | Nulos en `DEL` | Filas con `EDAD > 100` | `LN` en `EDAD > 100` | Filas con `NS > 0` | Total `NS` (No Especificados) | `SV > LN` | `SV < 0` |",
        "| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for _, r in q_df.iterrows():
        lines.append(
            f"| {int(r['anio'])} | {int(r['raw_rows']):,} | {int(r['nulls_def']):,} | {int(r['nulls_del']):,} | "
            f"{int(r['edad_gt_100_rows']):,} | {int(r['edad_gt_100_ln']):,} | {int(r['ns_gt_0_rows']):,} | "
            f"{int(r['ns_total']):,} | {int(r['part_gt_100_rows']):,} | {int(r['part_lt_0_rows']):,} |"
        )

    lines.extend(
        [
            "",
            "## 3. Hallazgos de Calidad y Reglas Aplicadas",
            "",
            "1. **Nulos en `DEL` (Distrito Electoral Local) en 2024:** Se detectaron valores nulos en la columna `DEL` en secciones electorales de 2024. Se normalizaron con el código `'SN'` (Sin Número/No especificado) sin afectar la agregación municipal (`cve_geo`) ni distrital federal (`DEF`).",
            "2. **Edades extremas (`EDAD > 100`):** Existen registros censales de personas con edades reportadas entre 101 y 125 años en el padrón. Al agrupar en el esquema unificado bajo el corte `rango_edad = '60+'`, se evita distorsión por valores extremos individuales sin perder un solo elector de la Lista Nominal.",
            "3. **Registros No Especificados (`NS > 0`):** Corresponden a cuadernillos no disponibles para captura o requeridos por autoridades jurisdiccionales. Se preservan explícitamente en la columna `no_especificados`.",
            "4. **Regla de Privacidad (`< 10`):** Toda celda en el esquema unificado con `lista_nominal < 10` (o `< 10` votantes en modalidades sin LN) lleva la bandera `celda_pequena_lt10 = true`, y en las vistas analíticas (`v_municipio_eleccion`, `v_distrito_eleccion`) las tasas de subgrupos con denominador `< 10` se suprimen (`NULL`).",
            "",
            "## 4. Tabla Puente Municipio-Año (`puente_municipio_anio`)",
            "",
            f"- **Total de claves municipales únicas (`cve_geo`) 2009–2024:** {len(bridge_df):,}",
            f"- **Municipios con panel completo (6 de 6 elecciones):** {int(bridge_df['es_panel_completo'].sum()):,}",
            f"- **Municipios con cambio en el marco geográfico (nueva creación o fusión):** {int((~bridge_df['es_panel_completo']).sum()):,}",
            "",
            "### Desglose por Estatus del Marco Geográfico",
            "",
            "| Estatus | Número de Municipios |",
            "| :--- | ---: |",
        ]
    )

    for k, v in status_counts.items():
        lines.append(f"| `{k}` | {int(v):,} |")

    new_muns = bridge_df[~bridge_df["es_panel_completo"]].sort_values(["primer_anio", "cve_geo"])
    if not new_muns.empty:
        lines.extend(
            [
                "",
                "### Detalle de Municipios con Cambios de Marco Geográfico (2009–2024)",
                "",
                "| `cve_geo` | Entidad | Municipio | Primer Año | Último Año | Elecciones Presente | Estatus |",
                "| :---: | :--- | :--- | :---: | :---: | :---: | :--- |",
            ]
        )
        for _, m in new_muns.iterrows():
            lines.append(
                f"| `{m['cve_geo']}` | {m['nom_ent']} | {m['nom_mun']} | {int(m['primer_anio'])} | "
                f"{int(m['ultimo_anio'])} | {int(m['n_elecciones_presente'])} | `{m['estatus_marco_geografico']}` |"
            )

    (DOCS_DIR / "calidad_datos.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_ingest_pipeline() -> None:
    t0 = time.time()
    print("[Ingest] Iniciando pipeline de ingesta CCPC 2009-2024...")

    parquet_root = INTERIM_DIR / "ccpc_unificado"
    parquet_root.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    all_dfs: list[pd.DataFrame] = []
    all_controls: list[dict[str, Any]] = []
    all_quality: list[dict[str, Any]] = []

    for year in ORDINARY_YEARS:
        t_yr = time.time()
        df_year, ctrl_rows, q_stats = process_ordinary_year(year)
        all_controls.extend(ctrl_rows)
        all_quality.append(q_stats)

        if year == 2024:
            df_spec, ctrl_spec = process_special_2024()
            df_year = pd.concat([df_year, df_spec], ignore_index=True)
            all_controls.extend(ctrl_spec)

        # Guardar Parquet particionado por año
        year_dir = parquet_root / f"anio={year}"
        year_dir.mkdir(parents=True, exist_ok=True)
        out_file = year_dir / "data.parquet"
        df_to_save = df_year.drop(columns=["anio"])
        table = pa.Table.from_pandas(df_to_save, preserve_index=False)
        pq.write_table(table, out_file, compression="snappy")

        all_dfs.append(df_year)
        print(
            f"  -> Año {year} procesado en {time.time() - t_yr:.1f}s | "
            f"Filas crudas: {q_stats['raw_rows']:,} -> Filas unificadas: {len(df_year):,}"
        )

    df_all = pd.concat(all_dfs, ignore_index=True)
    bridge_df = build_geographic_bridge(df_all)
    bridge_path = PROCESSED_DIR / "puente_municipio_anio.parquet"
    bridge_df.to_parquet(bridge_path, index=False)

    control_df = pd.DataFrame(all_controls)
    control_path = INTERIM_DIR / "control_totales_fuente.parquet"
    control_df.to_parquet(control_path, index=False)

    create_duckdb_catalog(
        parquet_dir=parquet_root,
        bridge_path=bridge_path,
        control_path=control_path,
        duckdb_path=DUCKDB_PATH,
    )

    write_quality_report(all_quality, bridge_df, control_df)
    print(f"[Ingest] Pipeline finalizado con éxito en {time.time() - t0:.1f}s.")


if __name__ == "__main__":
    run_ingest_pipeline()
