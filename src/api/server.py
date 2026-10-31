from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from src.llm.text_to_sql import answer_data_question

BASE_DIR = Path(__file__).resolve().parents[2]
PUBLIC_DIR = BASE_DIR / "app" / "public"


class DashboardRequestHandler(SimpleHTTPRequestHandler):
    """Servidor HTTP ligero para el Dashboard (Modo Online/Offline Plan B) y endpoint /api/chat."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        # Silenciar logs repetitivos en pruebas automatizadas
        pass

    def do_POST(self) -> None:
        if self.path == "/api/chat":
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length).decode("utf-8")
            payload = json.loads(raw_body) if raw_body else {}
            question = str(payload.get("question", "")).strip()
            res = answer_data_question(question)
            body_bytes = json.dumps(res.model_dump(), ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body_bytes)))
            self.end_headers()
            self.wfile.write(body_bytes)
            return

        self.send_response(404)
        self.end_headers()


def run_server(port: int = 3000) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), DashboardRequestHandler)
    print(f"[Dashboard Server] Escuchando en http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
