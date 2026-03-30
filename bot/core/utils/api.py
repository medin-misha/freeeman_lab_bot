from __future__ import annotations

import io
import mimetypes
import re
from dataclasses import dataclass
from typing import Any

import aiohttp
from aiogram import Bot
from aiogram.types import Voice

from config import settings


@dataclass(slots=True)
class DownloadedFile:
    content: bytes
    content_type: str
    filename: str


class API:
    def __init__(self, url: str | None = None) -> None:
        self.url = (url or settings.api_url).rstrip("/")

    def build_url(self, path: str) -> str:
        return f"{self.url}/{path.lstrip('/')}"

    async def post(self, path: str, data: dict[str, Any]) -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.build_url(path), json=data) as response:
                response.raise_for_status()
                return await response.json()

    async def get(self, path: str) -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.build_url(path)) as response:
                response.raise_for_status()
                return await response.json()

    async def post_multipart(
        self,
        path: str,
        form: aiohttp.FormData,
        params: dict[str, Any] | None = None,
    ):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.build_url(path),
                data=form,
                params=params,
            ) as response:
                response.raise_for_status()
                return await response.json()


class UserAPI(API):
    async def add_user(
        self,
        username: str,
        email: str,
        phone: str,
        first_name: str,
        last_name: str,
        chat_id: str,
    ) -> dict[str, Any]:
        payload = {
            "username": username,
            "email": email,
            "phone": phone,
            "first_name": first_name,
            "last_name": last_name,
            "chat_id": chat_id,
        }
        return await self.post("/users", payload)

    async def get_user_bi_chat_id(self, chat_id: str) -> dict[str, Any]:
        return await self.get(f"/users?page=1&limit=10&search={chat_id}&field=chat_id")


class FileAPI(API):
    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str,
        folder: str = "voice_messages",
    ) -> dict[str, Any]:
        form = aiohttp.FormData()
        form.add_field(
            "file",
            file_bytes,
            filename=filename,
            content_type=content_type,
        )
        return await self.post_multipart(
            "/files",
            form=form,
            params={"folder": folder},
        )

    async def download_file(self, file_id: int) -> DownloadedFile:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.build_url(f"/files/{file_id}")) as response:
                response.raise_for_status()
                content = await response.read()
                content_type = response.headers.get(
                    "Content-Type",
                    "application/octet-stream",
                )
                filename = self._extract_filename(
                    response.headers.get("Content-Disposition")
                )

        return DownloadedFile(
            content=content,
            content_type=content_type,
            filename=filename or self._build_filename(file_id, content_type),
        )

    def _build_filename(self, file_id: int, content_type: str) -> str:
        mime_type = content_type.partition(";")[0].strip()
        extension = mimetypes.guess_extension(mime_type) or ".bin"
        return f"diagnostic_{file_id}{extension}"

    def _extract_filename(self, content_disposition: str | None) -> str | None:
        if not content_disposition:
            return None

        match = re.search(r'filename="?(?P<filename>[^";]+)"?', content_disposition)
        if match is None:
            return None

        filename = match.group("filename").strip()
        return filename or None


class DiagnosticsAPI(API):
    async def voice_to_bytes(self, voice: Voice, bot: Bot):
        if voice is None:
            raise ValueError("Voice is None")
        tg_file = await bot.get_file(voice.file_id)
        buffer = io.BytesIO()
        await bot.download_file(tg_file.file_path, destination=buffer)
        buffer.seek(0)
        return buffer.getvalue()

    async def create_diagnostic(
        self,
        voice: Voice,
        bot: Bot,
        chat_id: str,
    ) -> dict[str, Any]:
        user_api = UserAPI()
        user = await user_api.get_user_bi_chat_id(chat_id)
        file_api = FileAPI()
        file_bytes: bytes = await self.voice_to_bytes(voice, bot)
        file = await file_api.upload_file(file_bytes, "voice_message.ogg", "audio/ogg")
        payload = {
            "file_id": file["id"],
            "user_id": user[0]["id"],
        }
        return await self.post("/diagnostics", payload)

    async def get_diagnostic_by_id(self, diagnostic_id: int) -> dict[str, Any]:
        return await self.get(f"/diagnostics/{diagnostic_id}")
