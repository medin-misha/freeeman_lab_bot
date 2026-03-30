from aiobotocore.session import get_session
from contextlib import asynccontextmanager
from pathlib import Path
import re
import unicodedata
from .error_handlers import S3ErrorHandler
from config import settings


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


def _transliterate_to_s3_safe(value: str | None, allow_slash: bool = False) -> str:
    if not value:
        return ""

    transliterated = "".join(
        CYRILLIC_TO_LATIN.get(char.lower(), char) for char in value
    )
    normalized = unicodedata.normalize("NFKD", transliterated).encode(
        "ascii", "ignore"
    ).decode("ascii")

    allowed_pattern = r"[^A-Za-z0-9._/-]+" if allow_slash else r"[^A-Za-z0-9._-]+"
    sanitized = re.sub(allowed_pattern, "_", normalized)
    sanitized = re.sub(r"_+", "_", sanitized).strip("._/")
    return sanitized


def _slugify_filename(filename: str | None) -> str:
    if not filename:
        return ""

    path = Path(filename)
    extension = "".join(path.suffixes)
    stem = path.name[: -len(extension)] if extension else path.name
    stem = _decode_hex_like_filename(stem)

    transliterated = "".join(
        CYRILLIC_TO_LATIN.get(char.lower(), char) for char in stem
    )
    normalized = unicodedata.normalize("NFKD", transliterated).encode(
        "ascii", "ignore"
    ).decode("ascii")

    slug = re.sub(r"[^A-Za-z0-9]+", "-", normalized.lower())
    slug = re.sub(r"-+", "-", slug).strip("-") or "file"
    return f"{slug}{extension}"


def build_download_filename(filename: str | None) -> str:
    return _slugify_filename(filename)


def _decode_hex_like_filename(value: str) -> str:
    parts = value.split("_")
    hex_tokens = [part for part in parts if re.fullmatch(r"[0-9a-fA-F]{2}", part)]
    if len(hex_tokens) < 4:
        return value

    decoded_parts: list[str] = []
    byte_buffer = bytearray()

    def flush_bytes() -> None:
        if not byte_buffer:
            return

        try:
            decoded_parts.append(byte_buffer.decode("utf-8"))
        except UnicodeDecodeError:
            decoded_parts.extend(f"{byte:02x}" for byte in byte_buffer)
        finally:
            byte_buffer.clear()

    for part in parts:
        if re.fullmatch(r"[0-9a-fA-F]{2}", part):
            byte_buffer.append(int(part, 16))
            continue

        flush_bytes()
        decoded_parts.append(part)

    flush_bytes()
    return "".join(decoded_parts)


class S3Client:
    def __init__(
        self,
        bucket_name: str = settings.s3.bucket_name,
        endpoint_url: str = settings.s3.endpoint_url,
        aws_access_key_id: str = settings.s3.access_key,
        aws_secret_access_key: str = settings.s3.secret_key,
    ):
        self.config: dict = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name: str = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
        self, file: bytes, object_name: str, folder: str = None, filename: str = None
    ):
    
        safe_folder = _transliterate_to_s3_safe(folder, allow_slash=True)
        safe_object_name = _transliterate_to_s3_safe(object_name)
        safe_filename = _slugify_filename(filename)

        key = f"{safe_object_name}{safe_filename}"
        if safe_folder:
            key = f"{safe_folder}/{key}"
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=file,
                )
        except Exception as e:
            S3ErrorHandler.handle(e, "upload file")
        else:
            return key

    async def get_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                return await response["Body"].read()
        except Exception as e:
            S3ErrorHandler.handle(e, "get file")
