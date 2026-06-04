from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path


DEFAULT_MESSAGE = "本番 API の単発疎通テストです。短く返信してください。"


def write_summary(status: str, reason: str | None = None, output_path: str | None = None) -> None:
    Path("outputs").mkdir(parents=True, exist_ok=True)
    summary = {
        "status": status,
        "reason": reason,
        "output_path": output_path,
        "generated_at_unix": int(time.time()),
        "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    }
    Path("outputs/live-smoke-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    if not os.getenv("OPENAI_API_KEY"):
        reason = "OPENAI_API_KEY is not set. Skipping live smoke test."
        print(reason)
        write_summary("skipped", reason=reason)
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
    code = subprocess.call(command)
    write_summary("passed" if code == 0 else "failed", output_path=str(output))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
