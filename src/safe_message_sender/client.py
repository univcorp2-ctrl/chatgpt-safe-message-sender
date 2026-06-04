from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


class MessageSenderError(RuntimeError):
    """Base error for sender failures."""


class MissingApiKeyError(MessageSenderError):
    """Raised when live execution is requested without an API key."""


class ApiRequestError(MessageSenderError):
    """Raised when the OpenAI API returns a non-successful response."""

    def __init__(self, status_code: int, message: str, response_body: Any | None = None) -> None:
        super().__init__(f"OpenAI API request failed with HTTP {status_code}: {message}")
        self.status_code = status_code
        self.response_body = response_body


@dataclass(frozen=True)
class ResponseResult:
    """Normalized response returned by the sender."""

    response_id: str | None
    status: str | None
    output_text: str
    raw: dict[str, Any]


def build_response_payload(
    message: str,
    model: str,
    instructions: str | None = None,
    metadata: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build a minimal Responses API payload.

    The payload intentionally represents a single, user-initiated message. It does not include
    retry loops, scraping logic, browser automation, or stealth behavior.
    """
    clean_message = message.strip()
    if not clean_message:
        raise ValueError("message must not be empty")

    payload: dict[str, Any] = {
        "model": model,
        "input": clean_message,
    }
    if instructions:
        payload["instructions"] = instructions
    if metadata:
        payload["metadata"] = metadata
    return payload


def extract_output_text(raw_response: dict[str, Any]) -> str:
    """Extract text from common Responses API response shapes."""
    direct = raw_response.get("output_text")
    if isinstance(direct, str):
        return direct

    chunks: list[str] = []
    for item in raw_response.get("output", []) or []:
        for content in item.get("content", []) or []:
            text = content.get("text")
            if isinstance(text, str):
                chunks.append(text)
    return "\n".join(chunks)


class OpenAIResponseClient:
    """Small sync client for OpenAI Responses API."""

    def __init__(
        self,
        api_key: str | None,
        base_url: str = "https://api.openai.com/v1",
        timeout_seconds: float = 60.0,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.http_client = http_client

    def send_message(
        self,
        message: str,
        model: str,
        instructions: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> ResponseResult:
        """Send one message to OpenAI Responses API and return a normalized result."""
        if not self.api_key:
            raise MissingApiKeyError("OPENAI_API_KEY is required when --execute is used")

        payload = build_response_payload(
            message=message,
            model=model,
            instructions=instructions,
            metadata=metadata,
        )
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "chatgpt-safe-message-sender/0.1.0",
        }

        client = self.http_client or httpx.Client(timeout=self.timeout_seconds)
        should_close = self.http_client is None
        try:
            response = client.post(
                f"{self.base_url}/responses",
                headers=headers,
                json=payload,
                timeout=self.timeout_seconds,
            )
        finally:
            if should_close:
                client.close()

        try:
            body: dict[str, Any] = response.json()
        except ValueError:
            body = {"raw_text": response.text}

        if response.status_code >= 400:
            error_message = "unknown error"
            if isinstance(body.get("error"), dict):
                error_message = str(body["error"].get("message", error_message))
            raise ApiRequestError(response.status_code, error_message, body)

        return ResponseResult(
            response_id=body.get("id") if isinstance(body.get("id"), str) else None,
            status=body.get("status") if isinstance(body.get("status"), str) else None,
            output_text=extract_output_text(body),
            raw=body,
        )
