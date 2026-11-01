from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from src.llm.text_to_sql import answer_data_question

BASE_DIR = Path(__file__).resolve().parents[2]
PUBLIC_DIR = BASE_DIR / "app" / "public"
DATA_DIR = PUBLIC_DIR / "data"

_JSON_CACHE: dict[str, dict[str, Any]] = {}


def _load_json(filename: str) -> dict[str, Any]:
    if filename in _JSON_CACHE:
        return _JSON_CACHE[filename]
    path = DATA_DIR / filename
    if not path.exists():
        path = BASE_DIR / "data" / "processed" / filename
    data = json.loads(path.read_text(encoding="utf-8"))
    _JSON_CACHE[filename] = data
    return data


class DashboardRequestHandler(SimpleHTTPRequestHandler):
    """
    Servidor REST API + Static Asset Server (Prompt A5):
    Soporta /api/profiles, /api/municipios, /api/municipio/{cve}, /api/transitions,
    /api/forecast, /api/simulate, /api/insights, /api/chat (/ask) y archivos estáticos.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        pass

    def _send_json(self, data: Any, status: int = 200) -> None:
        body_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.end_headers()
        self.wfile.write(body_bytes)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path.rstrip("/")

        if route in ("/api/profiles", "/profiles"):
            char_data = _load_json("perfiles_caracterizacion.json")
            llm_data = _load_json("llm_perfiles_narrativas_estrategias.json")
            self._send_json(
                {
                    "perfiles": char_data.get("perfiles", []),
                    "narrativas": llm_data.get("narrativas_perfiles", []),
                    "estrategias": llm_data.get("estrategias_perfiles", []),
                }
            )
            return

        if route in ("/api/municipios", "/municipios"):
            bundle = _load_json("municipios_bundle.json")
            self._send_json({"municipios": bundle.get("municipios", [])})
            return

        if route.startswith("/api/municipio/") or route.startswith("/municipio/"):
            cve = route.split("/")[-1].strip().zfill(5)
            bundle = _load_json("municipios_bundle.json")
            muns = bundle.get("municipios", [])
            found = next((m for m in muns if m["cve_geo"] == cve), None)
            if not found:
                self._send_json({"error": f"Municipio {cve} no encontrado"}, status=404)
                return
            self._send_json(found)
            return

        if route in ("/api/transitions", "/transitions"):
            self._send_json(_load_json("transiciones.json"))
            return

        if route in ("/api/forecast", "/forecast"):
            self._send_json(_load_json("simulador_what_if.json"))
            return

        if route in ("/api/insights", "/insights"):
            llm_data = _load_json("llm_perfiles_narrativas_estrategias.json")
            self._send_json({"insights": llm_data.get("insights_verificados_sql", [])})
            return

        # Servir archivos estáticos directamente con Content-Length explícito (evita bloqueo de mimetypes en Windows)
        rel_path = parsed.path.lstrip("/") or "index.html"
        static_file = (PUBLIC_DIR / rel_path).resolve()
        if static_file.is_file() and str(static_file).startswith(str(PUBLIC_DIR.resolve())):
            ext = static_file.suffix.lower()
            mime_map = {
                ".html": "text/html; charset=utf-8",
                ".css": "text/css; charset=utf-8",
                ".js": "application/javascript; charset=utf-8",
                ".json": "application/json; charset=utf-8",
                ".geojson": "application/geo+json; charset=utf-8",
                ".parquet": "application/octet-stream",
            }
            ctype = mime_map.get(ext, "application/octet-stream")
            body = static_file.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path.rstrip("/")
        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else ""
        payload = json.loads(raw_body) if raw_body else {}

        if route in ("/api/chat", "/api/ask", "/ask"):
            question = str(payload.get("question", "")).strip()
            res = answer_data_question(question)
            self._send_json(res.model_dump())
            return

        if route in ("/api/simulate", "/simulate"):
            sim_data = _load_json("simulador_what_if.json")
            cluster_id = int(payload.get("cluster_id", 0))
            delta_joven = float(payload.get("delta_joven_pp", 0.0))
            delta_inter = float(payload.get("delta_inter_pp", 0.0))
            delta_va = float(payload.get("delta_va_10k", 0.0))
            el_list = sim_data.get("elasticidades_por_perfil", [])
            el = next((x for x in el_list if int(x["cluster_id"]) == cluster_id), el_list[0])
            b_j = float(el["elasticidades_pp_sobre_part_2027"]["part_media_jovenes_18_29_por_1pp"])
            b_i = float(el["elasticidades_pp_sobre_part_2027"]["part_media_intermedia_por_1pp"])
            b_v = float(el["elasticidades_pp_sobre_part_2027"]["tasa_voto_anticipado_por_10_sobre_10k"])
            delta_part_pp = round(delta_joven * b_j + delta_inter * b_i + (delta_va / 10.0) * b_v, 3)
            ln_c = int(el["ln_2027_perfil"])
            nuevos_vot = int(round((delta_part_pp / 100.0) * ln_c))
            self._send_json(
                {
                    "cluster_id": cluster_id,
                    "delta_part_2027_pp": delta_part_pp,
                    "intervalo_80_pp": [round(delta_part_pp * 0.72, 3), round(delta_part_pp * 1.28, 3)],
                    "votantes_adicionales_estimados": nuevos_vot,
                    "aviso_no_causal": sim_data.get("aviso_metodologico_no_causal", ""),
                }
            )
            return

        self.send_response(404)
        self.end_headers()


def run_server(port: int = 3000) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), DashboardRequestHandler)
    print(f"[Dashboard Server] Escuchando en http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
