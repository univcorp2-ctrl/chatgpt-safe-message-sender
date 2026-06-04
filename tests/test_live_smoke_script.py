from __future__ import annotations

import json
from pathlib import Path

from scripts import live_smoke_test


def test_live_smoke_skips_without_api_key(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    code = live_smoke_test.main()

    assert code == 0
    summary = json.loads(Path("outputs/live-smoke-summary.json").read_text(encoding="utf-8"))
    assert summary["status"] == "skipped"
    assert "OPENAI_API_KEY" in summary["reason"]
