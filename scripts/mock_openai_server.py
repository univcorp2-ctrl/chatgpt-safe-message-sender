from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class MockOpenAIHandler(BaseHTTPRequestHandler):
    server_version = "MockOpenAI/0.1"

    def do_POST(self) -> None:  # noqa: N802
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length else b"{}"
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(400, {"error": {"message": "invalid json"}})
            return

        if self.path != "/v1/responses":
            self._send_json(404, {"error": {"message": "not found"}})
            return
        if not self.headers.get("Authorization", "").startswith("Bearer "):
            self._send_json(401, {"error": {"message": "missing bearer token"}})
            return
        if not payload.get("input"):
            self._send_json(400, {"error": {"message": "input is required"}})
            return

        self._send_json(
            200,
            {
                "id": "resp_mock_001",
                "status": "completed",
                "output_text": f"mock reply to: {payload['input']}",
            },
        )

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_json(self, status_code: int, body: dict[str, object]) -> None:
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = HTTPServer((host, port), MockOpenAIHandler)
    print(f"Mock OpenAI server listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
