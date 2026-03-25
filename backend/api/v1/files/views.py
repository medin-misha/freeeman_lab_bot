from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from core.database import database
from service.files.crud import create_file, get_file_by_id
from contracts.files.schemas import FileReturn

router = APIRouter(prefix="/files", tags=["files"])

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]


@router.post("/", response_model=FileReturn, status_code=status.HTTP_201_CREATED)
async def upload_file_view(
    session: SessionDep,
    file: UploadFile = File(...),
    folder: str = "voice_messages",
) -> FileReturn:
    """
    Загрузка файла в S3 и сохранение ссылки в БД.
    """
    return await create_file(session=session, file=file, folder=folder)


@router.get("/{file_id}")
async def get_file_view(
    session: SessionDep,
    file_id: int,
) -> StreamingResponse:
    return await get_file_by_id(session=session, file_id=file_id)