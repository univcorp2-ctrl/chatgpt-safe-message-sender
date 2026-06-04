FROM python:3.11-slim AS test

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY sample_messages ./sample_messages
COPY scripts ./scripts

RUN python -m pip install --upgrade pip \
    && pip install -e .[dev] \
    && ruff check . \
    && ruff format --check . \
    && pytest \
    && safe-send --message-file sample_messages/hello.txt --output outputs/dry-run-payload.json

FROM python:3.11-slim AS runtime

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY src ./src
COPY sample_messages ./sample_messages
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir .

ENTRYPOINT ["safe-send"]
CMD ["--help"]
