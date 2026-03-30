import hashlib
import mimetypes
import re
from pathlib import PurePosixPath

from fastapi import Response, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.files.schemas import FileCreate, FileReturn
from core.models.file import File
from service import CRUD
from service.s3 import S3Client, build_download_filename


async def create_file(
    session: AsyncSession,
    file: UploadFile,
    folder: str = "voice_messages",
) -> FileReturn:
    s3_client = S3Client()
    raw_file = await file.read()
    object_name = hashlib.md5(raw_file).hexdigest()
    link = await s3_client.upload_file(
        file=raw_file,
        object_name=object_name,
        folder=folder,
        filename=file.filename,
    )
    return await CRUD.create(session=session, model=File, data=FileCreate(link=link))


async def get_file_by_id(session: AsyncSession, file_id: int) -> Response:
    file_info = await CRUD.get(
        session=session,
        model=File,
        id=file_id,
    )
    s3_client = S3Client()
    content = await s3_client.get_file(object_name=file_info.link)
    mime_type, _ = mimetypes.guess_type(file_info.link)
    filename = _extract_filename_from_storage_key(file_info.link)
    headers = {"Cache-Control": "public, max-age=86400"}

    if filename is not None:
        headers["Content-Disposition"] = f'attachment; filename="{filename}"'

    return Response(
        content=content,
        media_type=mime_type or "application/octet-stream",
        headers=headers,  # Cache the file in clients for one day.
    )


def _extract_filename_from_storage_key(storage_key: str) -> str | None:
    basename = PurePosixPath(storage_key).name
    if not basename:
        return None

    stripped_basename = re.sub(r"^[0-9a-f]{32}", "", basename, count=1)
    candidate = stripped_basename or basename
    normalized = build_download_filename(candidate)
    return normalized or candidate
