# Test Matrix

| Layer | Command | Network | Requires API key | Purpose |
| --- | --- | --- | --- | --- |
| Unit tests | `pytest tests/test_client.py tests/test_cli.py` | No | No | Payload, CLI, response parsing, error handling |
| Mock integration | `pytest tests/test_integration_mock_api.py` | Localhost only | No | `--execute` live path against local mock API |
| Smoke skip check | `pytest tests/test_live_smoke_script.py` | No | No | Secret 未設定時も summary が残ること |
| Full local verify | `make verify` | No | No | lint, format, pytest, dry-run |
| Report verify | `make report` | No | No | JSON/JUnit レポート生成 |
| Docker build gate | `docker build -t chatgpt-safe-message-sender:local .` | Package install only | No | image build 中に検証を強制 |
| Live smoke | `python scripts/live_smoke_test.py` | Yes | Yes | 本番 OpenAI API への単発疎通 |

## 完了判定

- API key なし: `make verify` と `make report` が成功し、`outputs/validation-report.json` の `ok` が `true`
- API key あり: 上記に加えて `python scripts/live_smoke_test.py` が成功し、`outputs/live-smoke-summary.json` の `status` が `passed`
