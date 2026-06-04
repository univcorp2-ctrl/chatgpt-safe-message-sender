#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -e .[dev]
ruff check .
ruff format --check .
pytest
safe-send --message-file sample_messages/hello.txt --output outputs/dry-run-payload.json
cat outputs/dry-run-payload.json
