# Production Readiness

## 完成状態の定義

このリポジトリでは、次をすべて満たす状態を完成状態とします。

1. Web UI 自動操作ではなく、公式 API 経由で指定文言を送れる
2. dry-run で API 送信前の payload を確認できる
3. mock API integration test で live 実行経路を検証できる
4. `OPENAI_API_KEY` を設定すれば本番 API に単発送信できる
5. CI 相当の検証を `make verify` / `make report` / `bash scripts/run_local_ci.sh` / `docker build` で実行できる
6. GitHub Actions workflow は `docs/workflows` に保存済みで、workflow scope 復旧後に配置できる

## 検証コマンド

```bash
make verify
```

レポート付きで確認する場合:

```bash
make report
```

生成物:

- `outputs/validation-report.json`
- `outputs/pytest-junit.xml`
- `outputs/dry-run-payload.json`

または:

```bash
bash scripts/run_until_green.sh
```

Docker build でも lint、format、pytest、dry-run が通らないと image 作成が止まります。

```bash
docker build -t chatgpt-safe-message-sender:local .
```

## 本番API単発テスト

```bash
export OPENAI_API_KEY="sk-..."
safe-send --message "本番APIの単発テストです。短く返信してください。" --execute --output outputs/response.json
```

または、summary 付き smoke test:

```bash
python scripts/live_smoke_test.py
```

生成物:

- `outputs/live-smoke-summary.json`
- `outputs/live-smoke-response.json`（API key 設定時のみ）

## なぜブラウザ自動操作ではないか

ChatGPT Web UI を人間に見せかけて操作したり、検知回避を目的にマウス移動・タイピング遅延・User-Agent 偽装を行ったりする実装は、安全性と利用規約上のリスクが高いため、このプロジェクトでは採用しません。公式 API を使うことで、認証、監査、エラー処理、負荷制御が明確になります。
