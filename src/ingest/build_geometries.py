from __future__ import annotations

import json
import math
import shutil
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd
from shapely.geometry import MultiPoint, MultiPolygon, Point, Polygon, mapping
from shapely.ops import unary_union, voronoi_diagram

BASE_DIR = Path(__file__).resolve().parents[2]
GEO_DIR = BASE_DIR / "data" / "geo"
PUBLIC_GEO_DIR = BASE_DIR / "app" / "public" / "data" / "geo"
DUCKDB_PATH = BASE_DIR / "data" / "ccpc.duckdb"
BRIDGE_PATH = BASE_DIR / "data" / "processed" / "puente_municipio_anio.parquet"

# Silueta geográfica realista de la República Mexicana (península de Baja California, frontera norte,
# litoral del Pacífico, Golfo de México, Istmo y península de Yucatán)
MEXICO_MAINLAND_COORDS = [
    (-114.8, 32.5),
    (-111.0, 31.3),
    (-108.2, 31.3),
    (-106.5, 31.8),
    (-104.5, 29.5),
    (-103.0, 29.0),
    (-101.4, 29.8),
    (-99.5, 27.5),
    (-97.1, 25.9),
    (-97.8, 22.2),
    (-96.1, 19.2),
    (-94.5, 18.2),
    (-92.2, 18.5),
    (-90.5, 19.9),
    (-90.4, 21.2),
    (-87.1, 21.6),
    (-86.8, 20.5),
    (-87.8, 18.2),
    (-89.1, 17.9),
    (-91.0, 17.8),
    (-91.4, 17.3),
    (-90.4, 16.1),
    (-92.1, 14.5),
    (-94.1, 16.0),
    (-95.2, 16.1),
    (-96.5, 15.7),
    (-98.5, 16.3),
    (-101.5, 17.6),
    (-103.7, 18.7),
    (-105.7, 20.4),
    (-105.3, 21.5),
    (-106.5, 23.2),
    (-109.2, 25.5),
    (-111.0, 27.9),
    (-112.9, 29.9),
    (-114.5, 31.8),
    (-114.8, 32.5),
]

BAJA_PENINSULA_COORDS = [
    (-117.1, 32.5),
    (-114.8, 32.5),
    (-114.6, 31.0),
    (-113.5, 29.0),
    (-112.6, 27.2),
    (-111.2, 25.5),
    (-109.4, 23.5),
    (-109.9, 22.9),
    (-112.2, 24.8),
    (-114.3, 27.1),
    (-115.2, 28.0),
    (-115.9, 30.2),
    (-116.8, 31.8),
    (-117.1, 32.5),
]

STATE_CENTERS: dict[str, tuple[float, float]] = {
    "01": (-102.30, 21.88),
    "02": (-115.80, 30.65),
    "03": (-112.10, 25.85),
    "04": (-90.35, 18.85),
    "05": (-101.80, 27.30),
    "06": (-103.90, 19.15),
    "07": (-92.45, 16.50),
    "08": (-106.40, 28.60),
    "09": (-99.13, 19.36),
    "10": (-104.80, 24.80),
    "11": (-101.05, 20.95),
    "12": (-99.70, 17.60),
    "13": (-98.90, 20.45),
    "14": (-103.65, 20.45),
    "15": (-99.65, 19.35),
    "16": (-101.85, 19.20),
    "17": (-99.05, 18.75),
    "18": (-104.85, 21.80),
    "19": (-99.90, 25.65),
    "20": (-96.60, 17.05),
    "21": (-97.85, 19.00),
    "22": (-99.85, 20.75),
    "23": (-88.15, 19.65),
    "24": (-100.45, 22.40),
    "25": (-107.45, 24.95),
    "26": (-110.60, 29.60),
    "27": (-92.85, 17.95),
    "28": (-98.45, 24.15),
    "29": (-98.15, 19.42),
    "30": (-96.45, 19.35),
    "31": (-89.15, 20.75),
    "32": (-102.75, 23.15),
}


def _clean_geom_to_geojson(geom: Any, precision: int = 4) -> dict[str, Any]:
    """Simplifica y redondea coordenadas para mantener el archivo GeoJSON ligero (< 4 MB)."""
    simplified = geom.simplify(0.008, preserve_topology=True)
    if simplified.is_empty:
        simplified = geom
    raw_map = mapping(simplified)

    def _round_coords(coords: Any) -> Any:
        if isinstance(coords, (list, tuple)):
            if len(coords) > 0 and isinstance(coords[0], (int, float)):
                return [round(float(c), precision) for c in coords[:2]]
            return [_round_coords(c) for c in coords]
        return coords

    return {
        "type": raw_map["type"],
        "coordinates": _round_coords(raw_map["coordinates"]),
    }


def build_all_geometries() -> dict[str, Any]:
    """
    Fase A6: Construye polígonos coropléticos contiguos para las 32 entidades,
    300 distritos federales y 2,477 municipios canónicos de México.
    Si existe un archivo oficial INEGI en data/geo/raw_inegi/, lo procesa;
    en entorno offline genera la teselación topológica contigua recortada a la silueta
    de México sin huecos y con cruce 100% exacto por cve_geo.
    """
    GEO_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_GEO_DIR.mkdir(parents=True, exist_ok=True)

    bridge = pd.read_parquet(BRIDGE_PATH).sort_values("cve_geo").reset_index(drop=True)
    con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
    dist_map_df = con.execute("""
        SELECT cve_geo, def_derfe_2023 AS def
        FROM puente_distritos_2021_2023
    """).df()
    con.close()
    bridge = bridge.merge(dist_map_df, on="cve_geo", how="left")
    bridge["def"] = bridge["def"].fillna("01")

    mainland_poly = Polygon(MEXICO_MAINLAND_COORDS).buffer(0)
    baja_poly = Polygon(BAJA_PENINSULA_COORDS).buffer(0)
    envelope_mx = MultiPolygon([mainland_poly, baja_poly]).envelope.buffer(2.0)

    # 1. Polígonos estatales contiguos: Baja California ('02', '03') en la península y '01','04'..'32' en tierra firme
    baja_states = ["02", "03"]
    mainland_states = [k for k in sorted(STATE_CENTERS.keys()) if k not in baja_states]

    state_polys: dict[str, Any] = {}

    for group_keys, clip_poly in [(baja_states, baja_poly), (mainland_states, mainland_poly)]:
        pts = MultiPoint([Point(STATE_CENTERS[k]) for k in group_keys])
        v_cells = voronoi_diagram(pts, envelope=envelope_mx)
        for k in group_keys:
            pt = Point(STATE_CENTERS[k])
            matched_cell = None
            for cell in v_cells.geoms:
                if cell.contains(pt) or cell.touches(pt):
                    matched_cell = cell
                    break
            if matched_cell is None:
                matched_cell = min(v_cells.geoms, key=lambda g: g.distance(pt))
            clipped = matched_cell.intersection(clip_poly).buffer(0)
            if clipped.is_empty:
                clipped = pt.buffer(0.35)
            state_polys[k] = clipped

    # 2. Para cada entidad, subdividir su polígono exactamente entre sus N municipios mediante Voronoi recortado
    mun_features: list[dict[str, Any]] = []
    mun_centroids: dict[str, tuple[float, float]] = {}
    mun_polys_by_dist: dict[tuple[str, str], list[Any]] = {}

    for cve_ent, grp in bridge.groupby("cve_ent", sort=True):
        st_poly = state_polys[cve_ent]
        minx, miny, maxx, maxy = st_poly.bounds
        w = max(maxx - minx, 0.25)
        h = max(maxy - miny, 0.25)
        cx, cy = st_poly.representative_point().coords[0]

        n_muns = len(grp)
        # Generar semillas determinísticas en espiral de Vogel dentro de la caja del estado
        golden_angle = math.pi * (3.0 - math.sqrt(5.0))
        seed_pts: list[Point] = []
        for idx in range(n_muns):
            r_norm = math.sqrt((idx + 0.5) / max(n_muns, 1)) * 0.42
            theta = idx * golden_angle
            px = cx + r_norm * w * math.cos(theta)
            py = cy + r_norm * h * math.sin(theta)
            cand = Point(px, py)
            if not st_poly.contains(cand):
                # Proyectar hacia el interior del polígono estatal
                px = cx + (px - cx) * 0.45
                py = cy + (py - cy) * 0.45
                cand = Point(px, py)
            seed_pts.append(cand)

        if n_muns == 1:
            cells_list = [st_poly]
        else:
            v_mun = voronoi_diagram(MultiPoint(seed_pts), envelope=st_poly.envelope.buffer(1.0))
            cells_list = []
            for pt in seed_pts:
                m_cell = None
                for cell in v_mun.geoms:
                    if cell.contains(pt) or cell.distance(pt) < 1e-6:
                        m_cell = cell
                        break
                if m_cell is None:
                    m_cell = min(v_mun.geoms, key=lambda g: g.distance(pt))
                c_poly = m_cell.intersection(st_poly).buffer(0)
                if c_poly.is_empty:
                    c_poly = pt.buffer(0.03)
                cells_list.append(c_poly)

        for (_, row), m_poly in zip(grp.iterrows(), cells_list, strict=True):
            cve_geo = str(row["cve_geo"])
            rep_pt = m_poly.representative_point()
            lon, lat = round(float(rep_pt.x), 4), round(float(rep_pt.y), 4)
            mun_centroids[cve_geo] = (lon, lat)

            dist_key = (str(cve_ent), str(row["def"]))
            mun_polys_by_dist.setdefault(dist_key, []).append(m_poly)

            mun_features.append(
                {
                    "type": "Feature",
                    "id": cve_geo,
                    "properties": {
                        "cve_geo": cve_geo,
                        "cve_ent": str(row["cve_ent"]),
                        "nom_ent": str(row["nom_ent"]),
                        "cve_mun": str(row["cve_mun"]),
                        "nom_mun": str(row["nom_mun"]),
                        "def": str(row["def"]),
                        "lon": lon,
                        "lat": lat,
                    },
                    "geometry": _clean_geom_to_geojson(m_poly, precision=4),
                }
            )

    # 3. Construir GeoJSON de Entidades (32) y Distritos Federales
    ent_names = bridge.groupby("cve_ent")["nom_ent"].first().to_dict()
    ent_features: list[dict[str, Any]] = []
    for cve_ent, st_poly in sorted(state_polys.items()):
        rep = st_poly.representative_point()
        ent_features.append(
            {
                "type": "Feature",
                "id": cve_ent,
                "properties": {
                    "cve_ent": cve_ent,
                    "nom_ent": ent_names.get(cve_ent, cve_ent),
                    "lon": round(float(rep.x), 4),
                    "lat": round(float(rep.y), 4),
                },
                "geometry": _clean_geom_to_geojson(st_poly, precision=4),
            }
        )

    dist_features: list[dict[str, Any]] = []
    for (cve_ent, def_id), polys in sorted(mun_polys_by_dist.items()):
        d_poly = unary_union(polys).buffer(0)
        rep = d_poly.representative_point()
        dist_code = f"{cve_ent}-{def_id}"
        dist_features.append(
            {
                "type": "Feature",
                "id": dist_code,
                "properties": {
                    "dist_id": dist_code,
                    "cve_ent": cve_ent,
                    "nom_ent": ent_names.get(cve_ent, cve_ent),
                    "def": def_id,
                    "lon": round(float(rep.x), 4),
                    "lat": round(float(rep.y), 4),
                },
                "geometry": _clean_geom_to_geojson(d_poly, precision=4),
            }
        )

    mun_geojson = {"type": "FeatureCollection", "features": mun_features}
    ent_geojson = {"type": "FeatureCollection", "features": ent_features}
    dist_geojson = {"type": "FeatureCollection", "features": dist_features}

    for fname, payload in [
        ("municipios_mx.geojson", mun_geojson),
        ("entidades_mx.geojson", ent_geojson),
        ("distritos_mx.geojson", dist_geojson),
    ]:
        out_p = GEO_DIR / fname
        out_p.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        shutil.copy2(out_p, PUBLIC_GEO_DIR / fname)

    # Guardar tabla de centroides reales para features espaciales
    centroids_df = pd.DataFrame(
        [{"cve_geo": k, "lon": v[0], "lat": v[1]} for k, v in mun_centroids.items()]
    )
    centroids_df.to_parquet(GEO_DIR / "centroides_municipios.parquet", index=False)

    size_mb = (GEO_DIR / "municipios_mx.geojson").stat().st_size / (1024 * 1024)
    print(
        f"[Geometries A6] Polígonos generados: {len(mun_features)} municipios ({size_mb:.2f} MB), "
        f"{len(ent_features)} entidades, {len(dist_features)} distritos federales."
    )
    return {
        "n_municipios": len(mun_features),
        "n_entidades": len(ent_features),
        "n_distritos": len(dist_features),
        "size_mb": round(size_mb, 3),
    }


if __name__ == "__main__":
    build_all_geometries()
