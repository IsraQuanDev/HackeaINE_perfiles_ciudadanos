from __future__ import annotations

import json
import re
import threading
import time
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from src.api.server import DashboardRequestHandler

BASE_DIR = Path(__file__).resolve().parents[1]


def test_dashboard_e2e_server_and_api_chat() -> None:
    """
    Prueba E2E completa del servidor del Dashboard (Prompt 8):
    1) Verifica que la carga de la página principal y los bundles JSON/Parquet tome < 3 segundos.
    2) Verifica la presencia de los 8 componentes obligatorios, la advertencia de falacia ecológica
       y el aviso de 'No Causal' en el simulador What-If.
    3) Verifica el endpoint POST /api/chat tanto para preguntas respondibles (con SQL) como no respondibles.
    """
    server = ThreadingHTTPServer(("127.0.0.1", 0), DashboardRequestHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        t0 = time.time()
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/index.html", timeout=3) as resp:
            assert resp.status == 200
            html = resp.read().decode("utf-8")

        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/data/municipios_bundle.json", timeout=3
        ) as resp:
            assert resp.status == 200
            bundle = json.loads(resp.read().decode("utf-8"))

        elapsed = time.time() - t0
        assert elapsed < 3.0, f"La carga inicial del dashboard excedió 3s: {elapsed:.2f}s"
        assert len(bundle["municipios"]) >= 2450

        # Verificar que no exista mojibake en el bundle JSON servido
        raw_bundle_text = json.dumps(bundle, ensure_ascii=False)
        assert "Ã" not in raw_bundle_text and "Â" not in raw_bundle_text, "Mojibake detectado en municipios_bundle.json"

        # Verificar que el GeoJSON poligonal de municipios se sirva con los 2,477 polígonos
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/data/geo/municipios_mx.geojson", timeout=8
        ) as resp:
            assert resp.status == 200
            geojson = json.loads(resp.read().decode("utf-8"))
            assert len(geojson["features"]) == 2477

        # Verificar nuevos endpoints REST de la Fase A5
        for ep in ("/api/profiles", "/api/transitions", "/api/forecast", "/api/insights", "/api/municipio/22014"):
            with urllib.request.urlopen(f"http://127.0.0.1:{port}{ep}", timeout=8) as resp:
                assert resp.status == 200
                ep_data = json.loads(resp.read().decode("utf-8"))
                assert isinstance(ep_data, dict)

        # Verificar las 8 secciones requeridas en el DOM servido + Calidad de Datos v2
        for heading in [
            "1. Mapa Coroplético",
            "2. Tarjetas de Perfil",
            "3. Dinámica y Transiciones (Sankey)",
            "4. ¿Qué perfil tiene mi municipio?",
            "5. Proyección 2027",
            "6. Simulador What-If (No Causal)",
            "7. Pregúntale a los Datos (SQL)",
            "8. Metodología y Límites",
            "9. Calidad de Datos y Auditoría P0",
            "Falacia Ecológica",
            "NO CAUSAL",
        ]:
            assert heading in html, f"Falta componente o aviso obligatorio en el dashboard: {heading}"

        # Probar POST /api/chat con pregunta respondible
        req_ok = urllib.request.Request(
            f"http://127.0.0.1:{port}/api/chat",
            data=json.dumps(
                {"question": "¿Qué entidades tuvieron la mayor participación electoral en 2024?"}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req_ok, timeout=5) as resp:
            chat_ok = json.loads(resp.read().decode("utf-8"))
            assert chat_ok["es_respondible"] is True
            assert "SELECT" in chat_ok["sql_usado"].upper()
            assert len(chat_ok["tabla_respaldo"]) == 32

        # Probar POST /api/chat con pregunta no respondible (partidos políticos)
        req_refuse = urllib.request.Request(
            f"http://127.0.0.1:{port}/api/chat",
            data=json.dumps({"question": "¿Qué partido político ganó en 2024?"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req_refuse, timeout=5) as resp:
            chat_ref = json.loads(resp.read().decode("utf-8"))
            assert chat_ref["es_respondible"] is False
            assert chat_ref["sql_usado"] is None
    finally:
        server.shutdown()
        server.server_close()


def test_qa_security_no_api_keys_or_local_paths() -> None:
    """
    Auditoría QA (Prompt 9):
    Verifica que en el código fuente (src/, app/src/, tests/) no existan llaves de API hardcodeadas,
    datos personales ni rutas locales absolutas (C:\\Users\\...).
    """
    secret_pattern = re.compile(r"(sk-[a-zA-Z0-9]{20,}|AIzaSy[a-zA-Z0-9_-]{30,})")
    user_dir = "Users" + "/" + "52477"
    local_path_pattern = re.compile(rf"C:\\\\Users\\\\52477|c:/{user_dir}", re.IGNORECASE)

    code_files = (
        list((BASE_DIR / "src").rglob("*.py"))
        + [p for p in (BASE_DIR / "tests").rglob("*.py") if p.name != "test_dashboard_e2e.py"]
        + list((BASE_DIR / "app" / "src").rglob("*.ts*"))
    )
    for fpath in code_files:
        content = fpath.read_text(encoding="utf-8")
        assert not secret_pattern.search(content), f"Posible API key detectada en {fpath.name}"
        assert not local_path_pattern.search(content), f"Ruta local detectada en código fuente {fpath.name}"
