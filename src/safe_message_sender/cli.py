from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from safe_message_sender.client import (
    ApiRequestError,
    MissingApiKeyError,
    OpenAIResponseClient,
    build_response_payload,
)


def _read_message(args: argparse.Namespace) -> str:
    if args.message and args.message_file:
        raise ValueError("Use either --message or --message-file, not both")
    if args.message_file:
        return Path(args.message_file).read_text(encoding="utf-8")
    if args.message:
        return args.message
    raise ValueError("Either --message or --message-file is required")


def _write_json(path: str | None, payload: dict[str, Any], pretty: bool = True) -> None:
    output = json.dumps(payload, ensure_ascii=False, indent=2 if pretty else None)
    if path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Send one explicit message via the OpenAI Responses API. Defaults to dry-run.",
    )
    parser.add_argument("--message", help="Message text to send")
    parser.add_argument("--message-file", help="Path to UTF-8 text file containing the message")
    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        help="OpenAI model name. Default: env OPENAI_MODEL or gpt-4.1-mini",
    )
    parser.add_argument("--instructions", help="Optional developer/system-style instructions")
    parser.add_argument(
        "--output",
        default="outputs/safe-message-output.json",
        help="Output JSON path. Default: outputs/safe-message-output.json",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually call the OpenAI API. Without this flag, only a dry-run payload is written.",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        help="OpenAI API base URL. Default: https://api.openai.com/v1",
    )
    parser.add_argument("--compact", action="store_true", help="Write compact JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        message = _read_message(args)
        if not args.execute:
            payload = build_response_payload(
                message=message,
                model=args.model,
                instructions=args.instructions,
                metadata={"source": "chatgpt-safe-message-sender", "mode": "dry-run"},
            )
            _write_json(
                args.output,
                {"mode": "dry-run", "would_send": payload},
                pretty=not args.compact,
            )
            print(f"Dry-run complete. Payload written to {args.output}")
            return 0

        client = OpenAIResponseClient(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=args.base_url,
        )
        result = client.send_message(
            message=message,
            model=args.model,
            instructions=args.instructions,
            metadata={"source": "chatgpt-safe-message-sender", "mode": "live"},
        )
        _write_json(
            args.output,
            {
                "mode": "live",
                "response_id": result.response_id,
                "status": result.status,
                "output_text": result.output_text,
                "raw": result.raw,
            },
            pretty=not args.compact,
        )
        print(f"Live request complete. Response written to {args.output}")
        return 0
    except (ValueError, MissingApiKeyError, ApiRequestError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
