# ChatGPT Safe Message Sender

ChatGPT の Web UI をブラウザ操作で自動化するのではなく、OpenAI の公式 Responses API を使って、指定した文言を安全に送信する CLI です。

> 重要: このリポジトリは、ChatGPT Web UI に対して「人間のように見せる」「検知を回避する」「ブロックされないように偽装する」ためのブラウザ自動操作を実装しません。代わりに、公式 API を用いた明示的で監査しやすい自動化を提供します。

## できること

- 指定文言を OpenAI Responses API に送信する
- `--execute` を付けない限り API 送信しない安全な dry-run
- 送信 payload または API 応答を JSON として保存
- GitHub Actions で lint / format check / test / dry-run artifact 生成
- 手動実行の live smoke workflow で、本番 API への単発疎通確認

## できないこと

- ChatGPT Web UI を Playwright / Selenium 等で操作すること
- CAPTCHA、レート制限、bot 検知、利用制限の回避
- 人間の操作に見せかけるマウス移動・タイピング偽装
- 大量送信、連続送信、スパム的な利用

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

API を実行する場合だけ、環境変数を設定します。

```bash
export OPENAI_API_KEY="sk-..."
```

## 使い方

### dry-run: 実送信せず payload を保存

```bash
safe-send --message "こんにちは。これはテストです。" --output outputs/payload.json
```

### 本番 API に単発送信

```bash
safe-send \
  --message "こんにちは。これは本番疎通テストです。" \
  --model gpt-4.1-mini \
  --execute \
  --output outputs/response.json
```

### ファイルから送信

```bash
safe-send --message-file sample_messages/hello.txt --execute --output outputs/response.json
```

## GitHub Actions

- `ci.yml`: push / pull_request / workflow_dispatch で lint、format check、test、dry-run artifact を実行
- `live-smoke.yml`: workflow_dispatch で `OPENAI_API_KEY` secret が設定されている場合だけ、本番 API に単発送信

Artifact 名:

- `safe-message-sender-dry-run-output`
- `safe-message-sender-live-smoke-output`

## Secrets

GitHub Actions の live smoke を使う場合のみ、Repository Secret に以下を設定します。

| Secret | 用途 |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI Responses API を呼び出すための API key |

## アーキテクチャ

```mermaid
flowchart LR
    U[User / GitHub Actions] --> CLI[safe-send CLI]
    CLI --> CFG[Config + Payload Builder]
    CLI -->|dry-run| ART[JSON Artifact]
    CLI -->|--execute| API[OpenAI Responses API]
    API --> RES[Response JSON]
    RES --> ART
```

詳しくは [`docs/architecture.md`](docs/architecture.md) を参照してください。

## 本番テストについて

このリポジトリは、本番 API を呼べる実装と手動 workflow を含みます。ただし、実際に OpenAI API を呼ぶには `OPENAI_API_KEY` が必要です。Secret が未設定の状態では、CI は mock / dry-run までを自動確認します。
