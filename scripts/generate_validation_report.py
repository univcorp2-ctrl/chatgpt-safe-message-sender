from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


COMMANDS: list[list[str]] = [
    [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
    ["ruff", "check", "."],
    ["ruff", "format", "--check", "."],
    ["pytest", "--junitxml", "outputs/pytest-junit.xml"],
    [
        "safe-send",
        "--message-file",
        "sample_messages/hello.txt",
        "--output",
        "outputs/dry-run-payload.json",
    ],
]


def run_command(command: list[str]) -> dict[str, Any]:
    started = time.time()
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    return {
        "command": command,
        "returncode": completed.returncode,
        "duration_seconds": round(time.time() - started, 3),
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
        "ok": completed.returncode == 0,
    }


def main() -> int:
    Path("outputs").mkdir(parents=True, exist_ok=True)
    results = []
    overall_ok = True

    for command in COMMANDS:
        result = run_command(command)
        results.append(result)
        if not result["ok"]:
            overall_ok = False
            break

    report = {
        "ok": overall_ok,
        "generated_at_unix": int(time.time()),
        "results": results,
        "artifacts": [
            "outputs/validation-report.json",
            "outputs/pytest-junit.xml",
            "outputs/dry-run-payload.json",
        ],
    }
    Path("outputs/validation-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
