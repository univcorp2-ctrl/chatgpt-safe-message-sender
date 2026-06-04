# Setup Guide

## 1. ローカル実行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 2. dry-run

API key なしで動きます。

```bash
safe-send --message "こんにちは" --output outputs/payload.json
```

## 3. 本番 API 実行

API key を環境変数に設定して、`--execute` を付けます。

```bash
export OPENAI_API_KEY="sk-..."
safe-send --message "こんにちは" --execute --output outputs/response.json
```

## 4. GitHub Actions の live smoke

Repository Settings → Secrets and variables → Actions → New repository secret で次を登録します。

- Name: `OPENAI_API_KEY`
- Secret: OpenAI API key の実値

その後、Actions → Live Smoke Test → Run workflow を実行します。

## 5. トラブルシューティング

| 症状 | 原因 | 対応 |
| --- | --- | --- |
| `OPENAI_API_KEY is required` | `--execute` 実行時に API key がない | 環境変数または GitHub Secret を設定 |
| HTTP 401 | API key が無効、または権限不足 | API key を確認 |
| HTTP 429 | レート制限 | 実行頻度を下げる。大量送信しない |
| output が空 | モデル応答形式に text が含まれない | `raw` JSON を確認 |
