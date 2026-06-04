from __future__ import annotations

import json
import threading
from http.server import HTTPServer
from pathlib import Path

from safe_message_sender.cli import main
from scripts.mock_openai_server import MockOpenAIHandler


def test_cli_execute_against_mock_openai_server(tmp_path: Path, monkeypatch) -> None:
    server = HTTPServer(("127.0.0.1", 0), MockOpenAIHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    output = tmp_path / "mock-live-response.json"
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    try:
        code = main(
            [
                "--message",
                "integration hello",
                "--base-url",
                f"http://127.0.0.1:{port}/v1",
                "--execute",
                "--output",
                str(output),
            ]
        )
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    assert code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["mode"] == "live"
    assert payload["response_id"] == "resp_mock_001"
    assert payload["status"] == "completed"
    assert "integration hello" in payload["output_text"]
