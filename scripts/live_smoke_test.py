from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


DEFAULT_MESSAGE = "本番 API の単発疎通テストです。短く返信してください。"


def main() -> int:
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set. Skipping live smoke test.")
        return 0

    output = Path("outputs/live-smoke-response.json")
    command = [
        sys.executable,
        "-m",
        "safe_message_sender.cli",
        "--message",
        os.getenv("LIVE_SMOKE_MESSAGE", DEFAULT_MESSAGE),
        "--model",
        os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        "--execute",
        "--output",
        str(output),
    ]
    print("Running one live Responses API smoke request...")
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
