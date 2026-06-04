from __future__ import annotations

import json
from pathlib import Path

from safe_message_sender.cli import main


def test_cli_dry_run_message(tmp_path: Path) -> None:
    output = tmp_path / "payload.json"
    code = main(["--message", "hello", "--output", str(output)])

    assert code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["mode"] == "dry-run"
    assert payload["would_send"]["input"] == "hello"


def test_cli_rejects_missing_message(tmp_path: Path) -> None:
    output = tmp_path / "payload.json"
    code = main(["--output", str(output)])

    assert code == 2
    assert not output.exists()


def test_cli_dry_run_message_file(tmp_path: Path) -> None:
    message_file = tmp_path / "message.txt"
    output = tmp_path / "payload.json"
    message_file.write_text("from file", encoding="utf-8")

    code = main(["--message-file", str(message_file), "--output", str(output)])

    assert code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["would_send"]["input"] == "from file"
