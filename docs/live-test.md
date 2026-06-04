# Live Test Policy

## 自動で実行されるテスト

通常の CI では、以下を自動確認します。

- Python package install
- ruff lint
- ruff format check
- pytest
- API key 不要の dry-run
- dry-run artifact upload

## 本番 API テスト

本番 API テストは `live-smoke.yml` に分離しています。理由は、API key と課金対象の API 呼び出しが必要なためです。

実行条件:

- GitHub Repository Secret `OPENAI_API_KEY` が設定済み
- Actions 画面から `Live Smoke Test` を手動実行

実行内容:

- 1 回だけ OpenAI Responses API に送信
- 応答 JSON を `safe-message-sender-live-smoke-output` artifact として保存

## 負荷配慮

- 自動スケジュール実行なし
- 連続送信なし
- secret がない場合は skip
- retry 連打なし
