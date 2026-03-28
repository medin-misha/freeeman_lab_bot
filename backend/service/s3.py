from aiobotocore.session import get_session
from contextlib import asynccontextmanager
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
    "й": "y",
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
        safe_filename = _transliterate_to_s3_safe(filename)

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
