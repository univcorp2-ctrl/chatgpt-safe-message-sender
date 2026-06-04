from __future__ import annotations

import httpx
import pytest

from safe_message_sender.client import (
    ApiRequestError,
    MissingApiKeyError,
    OpenAIResponseClient,
    build_response_payload,
    extract_output_text,
)


def test_build_response_payload_minimal() -> None:
    payload = build_response_payload(" hello ", "gpt-4.1-mini")
    assert payload == {"model": "gpt-4.1-mini", "input": "hello"}


def test_build_response_payload_rejects_empty_message() -> None:
    with pytest.raises(ValueError, match="message must not be empty"):
        build_response_payload("   ", "gpt-4.1-mini")


def test_extract_output_text_direct() -> None:
    assert extract_output_text({"output_text": "hello"}) == "hello"


def test_extract_output_text_nested() -> None:
    raw = {
        "output": [
            {"content": [{"text": "one"}, {"text": "two"}]},
            {"content": [{"text": "three"}]},
        ]
    }
    assert extract_output_text(raw) == "one\ntwo\nthree"


def test_send_message_requires_api_key() -> None:
    client = OpenAIResponseClient(api_key=None)
    with pytest.raises(MissingApiKeyError):
        client.send_message("hello", "gpt-4.1-mini")


def test_send_message_success_with_mock_transport() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/responses"
        assert request.headers["authorization"] == "Bearer test-key"
        return httpx.Response(
            200,
            json={"id": "resp_123", "status": "completed", "output_text": "mocked reply"},
        )

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as http_client:
        client = OpenAIResponseClient(api_key="test-key", http_client=http_client)
        result = client.send_message("hello", "gpt-4.1-mini")

    assert result.response_id == "resp_123"
    assert result.status == "completed"
    assert result.output_text == "mocked reply"


def test_send_message_api_error_with_mock_transport() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"error": {"message": "rate limit"}})

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as http_client:
        client = OpenAIResponseClient(api_key="test-key", http_client=http_client)
        with pytest.raises(ApiRequestError) as exc:
            client.send_message("hello", "gpt-4.1-mini")

    assert exc.value.status_code == 429
    assert "rate limit" in str(exc.value)
