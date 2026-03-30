from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any
from urllib.parse import unquote
import unicodedata

from aiogram.types import Message


CYRILLIC_TO_LATIN = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "j",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


@dataclass(slots=True)
class ResultCallbackData:
    diagnostic_id: int
    user_id: int


@dataclass(slots=True)
class TelegramAttachment:
    file_id: str
    filename: str
    content_type: str


def extract_diagnostic_id(obj: object) -> int | None:
    return _coerce_int(_extract_value(obj, "id"))


def extract_file_id(obj: object) -> int | None:
    return _coerce_int(_extract_value(obj, "file_id"))


def extract_user_id(obj: object) -> int | None:
    return _coerce_int(_extract_value(obj, "user_id"))


def build_display_name(username: str | None, user_id: int) -> str:
    if isinstance(username, str) and username.strip():
        return username.strip()

    return f"id={user_id}"


def build_result_callback_data(
    prefix: str,
    diagnostic_id: int,
    user_id: int,
) -> str:
    return f"{prefix}:{diagnostic_id}:{user_id}"


def parse_result_callback_data(
    data: object,
    prefix: str,
) -> ResultCallbackData | None:
    if not isinstance(data, str):
        return None

    expected_prefix = f"{prefix}:"
    if not data.startswith(expected_prefix):
        return None

    payload = data.removeprefix(expected_prefix).split(":")
    if len(payload) != 2:
        return None

    diagnostic_id = _coerce_int(payload[0])
    user_id = _coerce_int(payload[1])
    if diagnostic_id is None or user_id is None:
        return None

    return ResultCallbackData(diagnostic_id=diagnostic_id, user_id=user_id)


def extract_attachment(message: Message) -> TelegramAttachment | None:
    if message.document is not None:
        return TelegramAttachment(
            file_id=message.document.file_id,
            filename=_coerce_filename(
                message.document.file_name,
                message.document.file_id,
                "result.bin",
            ),
            content_type=_coerce_content_type(
                message.document.mime_type,
                "application/octet-stream",
            ),
        )

    if message.audio is not None:
        return TelegramAttachment(
            file_id=message.audio.file_id,
            filename=_coerce_filename(
                message.audio.file_name,
                message.audio.file_id,
                "result_audio.mp3",
            ),
            content_type=_coerce_content_type(
                message.audio.mime_type,
                "audio/mpeg",
            ),
        )

    return None


def _extract_value(obj: object, field_name: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(field_name)

    if hasattr(obj, field_name):
        return getattr(obj, field_name)

    return None


def _coerce_int(value: object) -> int | None:
    if isinstance(value, int):
        return value

    if isinstance(value, str) and value.isdigit():
        return int(value)

    return None


def _coerce_filename(value: object, file_id: str, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        normalized = _normalize_upload_filename(value.strip())
        return normalized or fallback or f"file_{file_id}"

    return fallback if fallback else f"file_{file_id}"


def _coerce_content_type(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()

    return fallback


def _normalize_upload_filename(filename: str) -> str:
    decoded = _decode_percent_encoded_filename(filename)
    path = Path(decoded)
    extension = "".join(path.suffixes).lower()
    stem = path.name[: -len(extension)] if extension else path.name

    transliterated = "".join(
        CYRILLIC_TO_LATIN.get(char.lower(), char) for char in stem
    )
    normalized = unicodedata.normalize("NFKD", transliterated).encode(
        "ascii",
        "ignore",
    ).decode("ascii")
    slug = re.sub(r"[^A-Za-z0-9]+", "-", normalized.lower())
    slug = re.sub(r"-+", "-", slug).strip("-") or "file"
    return f"{slug}{extension}"


def _decode_percent_encoded_filename(filename: str) -> str:
    if "%" not in filename:
        return filename

    decoded = unquote(filename)
    return decoded if decoded else filename
