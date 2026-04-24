from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.diagnostics import DiagnosticsCreate, DiagnosticsRead, DiagnosticsUpdate
from core import database
from core.models import Diagnostics, User
from service import CRUD
from service.diagnostic.publisher import (
    publish_diagnostic_request,
    publish_diagnostic_response,
)

router = APIRouter(tags=["diagnostics"], prefix="/diagnostics")

SessionDepends = Annotated[AsyncSession, Depends(database.get_session)]


@router.post("", response_model=DiagnosticsRead, status_code=status.HTTP_201_CREATED)
async def create_diagnostics(
    data: DiagnosticsCreate, session: SessionDepends
) -> Diagnostics:
    diagnostic = await CRUD.create(data=data, model=Diagnostics, session=session)
    await publish_diagnostic_request(DiagnosticsRead.model_validate(diagnostic))
    return diagnostic


@router.get("", response_model=list[DiagnosticsRead], status_code=status.HTTP_200_OK)
async def get_diagnostics(
    session: SessionDepends,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    search: str | None = None,
    field: str | None = None,
) -> list[Diagnostics]:
    return await CRUD.get(
        model=Diagnostics,
        session=session,
        page=page,
        limit=limit,
        search=search,
        field=field,
    )


@router.get("/{id}", response_model=DiagnosticsRead, status_code=status.HTTP_200_OK)
async def get_diagnostics_by_id(id: int, session: SessionDepends) -> Diagnostics:
    return await CRUD.get(model=Diagnostics, session=session, id=id)


@router.patch("/{id}", response_model=DiagnosticsRead, status_code=status.HTTP_200_OK)
async def patch_diagnostics(
    id: int, data: DiagnosticsUpdate, session: SessionDepends
) -> Diagnostics:
    diagnostic = await CRUD.patch(new_data=data, model=Diagnostics, session=session, id=id)

    if diagnostic.result_file_id is not None:
        user = await CRUD.get(model=User, session=session, id=diagnostic.user_id)
        await publish_diagnostic_response(
            chat_id=user.chat_id,
            file_id=diagnostic.result_file_id,
        )

    return diagnostic


@router.delete("/{id}", response_model=str, status_code=status.HTTP_200_OK)
async def delete_diagnostics(id: int, session: SessionDepends) -> str:
    return await CRUD.delete(model=Diagnostics, session=session, id=id)
