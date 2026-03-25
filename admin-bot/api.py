import mimetypes
from dataclasses import dataclass

import aiohttp


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


class BackendAPIClient:
    def __init__(self, api_url: str) -> None:
        self._base_url = api_url.rstrip("/")
        self._session: aiohttp.ClientSession | None = None

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def download_file(self, file_id: int) -> DownloadedFile:
        session = await self._get_session()
        async with session.get(
            f"{self._base_url}/files/{file_id}",
            timeout=aiohttp.ClientTimeout(total=35),
        ) as response:
            response.raise_for_status()
            content = await response.read()
            content_type = response.headers.get("Content-Type", "application/octet-stream")

        return DownloadedFile(
            content=content,
            content_type=content_type,
            filename=self._build_filename(file_id, content_type),
        )

    async def get_user(self, user_id: int) -> BackendUser:
        session = await self._get_session()
        async with session.get(
            f"{self._base_url}/users/{user_id}",
            timeout=aiohttp.ClientTimeout(total=35),
        ) as response:
            response.raise_for_status()
            payload = await response.json()

        return BackendUser(
            id=int(payload["id"]),
            username=payload.get("username"),
            chat_id=str(payload["chat_id"]),
        )

    async def upload_file(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str,
        folder: str = "diagnostic_results",
    ) -> UploadedBackendFile:
        session = await self._get_session()
        form = aiohttp.FormData()
        form.add_field(
            "file",
            file_bytes,
            filename=filename,
            content_type=content_type,
        )

        async with session.post(
            f"{self._base_url}/files",
            data=form,
            params={"folder": folder},
            timeout=aiohttp.ClientTimeout(total=35),
        ) as response:
            response.raise_for_status()
            payload = await response.json()

        return UploadedBackendFile(
            id=int(payload["id"]),
            link=str(payload["link"]),
        )

    async def get_diagnostic(self, diagnostic_id: int) -> BackendDiagnostic:
        session = await self._get_session()
        async with session.get(
            f"{self._base_url}/diagnostics/{diagnostic_id}",
            timeout=aiohttp.ClientTimeout(total=35),
        ) as response:
            response.raise_for_status()
            payload = await response.json()

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
        payload: dict[str, object | None],
    ) -> BackendDiagnostic:
        session = await self._get_session()
        async with session.patch(
            f"{self._base_url}/diagnostics/{diagnostic_id}",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=35),
        ) as response:
            response.raise_for_status()
            body = await response.json()

        return BackendDiagnostic(
            id=int(body["id"]),
            status=str(body["status"]),
            file_id=int(body["file_id"]),
            result_file_id=_coerce_optional_int(body.get("result_file_id")),
            passed_at=body.get("passed_at"),
            user_id=int(body["user_id"]),
        )

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

        return self._session

    def _build_filename(self, file_id: int, content_type: str) -> str:
        mime_type = content_type.partition(";")[0].strip()
        extension = mimetypes.guess_extension(mime_type) or ".bin"
        return f"voice_{file_id}{extension}"


def _coerce_optional_int(value: object) -> int | None:
    if value is None:
        return None

    return int(value)
