from __future__ import annotations

import mimetypes
from dataclasses import dataclass
from typing import Any

import aiohttp

from config import settings


REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=35)


@dataclass(slots=True)
class DownloadedFile:
    content: bytes
    content_type: str
    filename: str


@dataclass(slots=True)
class BackendUser:
    id: int
    username: str | None
    chat_id: str


@dataclass(slots=True)
class BackendDiagnostic:
    id: int
    status: str
    file_id: int
    result_file_id: int | None
    passed_at: str | None
    user_id: int


@dataclass(slots=True)
class UploadedBackendFile:
    id: int
    link: str


class API:
    def __init__(self, url: str | None = None) -> None:
        self.url = (url or settings.api_url).rstrip("/")

    def build_url(self, path: str) -> str:
        return f"{self.url}/{path.lstrip('/')}"

    async def get(self, path: str) -> dict[str, Any]:
        async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
            async with session.get(self.build_url(path)) as response:
                response.raise_for_status()
                return await response.json()

    async def post(
        self,
        path: str,
        data: dict[str, Any],
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
            async with session.post(
                self.build_url(path),
                json=data,
                params=params,
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def patch(self, path: str, data: dict[str, Any]) -> dict[str, Any]:
        async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
            async with session.patch(self.build_url(path), json=data) as response:
                response.raise_for_status()
                return await response.json()

    async def post_multipart(
        self,
        path: str,
        form: aiohttp.FormData,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
            async with session.post(
                self.build_url(path),
                data=form,
                params=params,
            ) as response:
                response.raise_for_status()
                return await response.json()


class UserAPI(API):
    async def get_user(self, user_id: int) -> BackendUser:
        payload = await self.get(f"/users/{user_id}")
        return BackendUser(
            id=int(payload["id"]),
            username=payload.get("username"),
            chat_id=str(payload["chat_id"]),
        )


class FileAPI(API):
    async def download_file(self, file_id: int) -> DownloadedFile:
        async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
            async with session.get(self.build_url(f"/files/{file_id}")) as response:
                response.raise_for_status()
                content = await response.read()
                content_type = response.headers.get(
                    "Content-Type",
                    "application/octet-stream",
                )

        return DownloadedFile(
            content=content,
            content_type=content_type,
            filename=self._build_filename(file_id, content_type),
        )

    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str,
        folder: str = "diagnostic_results",
    ) -> UploadedBackendFile:
        form = aiohttp.FormData()
        form.add_field(
            "file",
            file_bytes,
            filename=filename,
            content_type=content_type,
        )
        payload = await self.post_multipart(
            "/files",
            form=form,
            params={"folder": folder},
        )
        return UploadedBackendFile(
            id=int(payload["id"]),
            link=str(payload["link"]),
        )

    def _build_filename(self, file_id: int, content_type: str) -> str:
        mime_type = content_type.partition(";")[0].strip()
        extension = mimetypes.guess_extension(mime_type) or ".bin"
        return f"voice_{file_id}{extension}"


class DiagnosticsAPI(API):
    async def get_diagnostic_by_id(self, diagnostic_id: int) -> BackendDiagnostic:
        payload = await self.get(f"/diagnostics/{diagnostic_id}")
        return BackendDiagnostic(
            id=int(payload["id"]),
            status=str(payload["status"]),
            file_id=int(payload["file_id"]),
            result_file_id=_coerce_optional_int(payload.get("result_file_id")),
            passed_at=payload.get("passed_at"),
            user_id=int(payload["user_id"]),
        )

    async def patch_diagnostic(
        self,
        diagnostic_id: int,
        payload: dict[str, Any],
    ) -> BackendDiagnostic:
        body = await self.patch(f"/diagnostics/{diagnostic_id}", payload)
        return BackendDiagnostic(
            id=int(body["id"]),
            status=str(body["status"]),
            file_id=int(body["file_id"]),
            result_file_id=_coerce_optional_int(body.get("result_file_id")),
            passed_at=body.get("passed_at"),
            user_id=int(body["user_id"]),
        )


def _coerce_optional_int(value: object) -> int | None:
    if value is None:
        return None

    return int(value)
