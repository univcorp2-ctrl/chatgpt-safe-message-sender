# CODEX.md

## Project intent

Build and maintain a safe CLI for sending one explicit user message through the OpenAI Responses API.

## Non-goals

Do not add browser automation against ChatGPT Web UI. Do not implement stealth, bot detection bypass, CAPTCHA bypass, account automation, or human-like input simulation intended to evade restrictions.

## Development commands

```bash
pip install -e .[dev]
ruff check .
ruff format --check .
pytest
safe-send --message-file sample_messages/hello.txt --output outputs/dry-run-payload.json
```

## Safety notes

- Keep live calls behind `--execute`.
- Keep secrets out of the repo.
- Prefer dry-run and mocked tests in CI.
