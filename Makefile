.PHONY: install lint format-check test dry-run integration live-smoke verify docker-build clean

install:
	python -m pip install --upgrade pip
	pip install -e .[dev]

lint:
	ruff check .

format-check:
	ruff format --check .

test:
	pytest

dry-run:
	safe-send --message-file sample_messages/hello.txt --output outputs/dry-run-payload.json
	cat outputs/dry-run-payload.json

integration:
	pytest tests/test_integration_mock_api.py

live-smoke:
	python scripts/live_smoke_test.py

verify: install lint format-check test dry-run

docker-build:
	docker build -t chatgpt-safe-message-sender:local .

clean:
	rm -rf outputs .pytest_cache .ruff_cache build dist *.egg-info src/*.egg-info
