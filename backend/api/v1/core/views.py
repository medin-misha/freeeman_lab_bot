from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.core import CoreCreate, CoreFormSubmit, CoreRead, CoreUpdate
from contracts.user import UserUpdate
from core import database
from core.models import Core, User
from service import CRUD
from service.core import publish_core_application

router = APIRouter(tags=["core"], prefix="/core")
SessionDepends = Annotated[AsyncSession, Depends(database.get_session)]


@router.get("", response_model=list[CoreRead], status_code=status.HTTP_200_OK)
async def get_core(
    session: SessionDepends,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    search: str | None = None,
    field: str | None = None,
) -> list[Core]:
    return await CRUD.get(
        model=Core,
        session=session,
        page=page,
        limit=limit,
        search=search,
        field=field,
    )


@router.get("/{id}", response_model=CoreRead, status_code=status.HTTP_200_OK)
async def get_core_by_id(id: int, session: SessionDepends) -> Core:
    return await CRUD.get(model=Core, session=session, id=id)


@router.post("/submit", response_model=CoreRead, status_code=status.HTTP_201_CREATED)
async def submit_core_form(data: CoreFormSubmit, session: SessionDepends) -> Core:
    result = await session.execute(
        select(User).where(User.chat_id == data.telegram_id)
    )
    user: User | None = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with telegram_id={data.telegram_id} not found.",
        )

    await CRUD.patch(
        new_data=UserUpdate(
            full_name=data.full_name,
            birth_date=data.birth_date,
            city=data.city,
        ),
        model=User,
        session=session,
        id=user.id,
    )

    core = await CRUD.create(
        data=CoreCreate(
            user_id=user.id,
            activity=data.activity,
            request=data.request,
            priorities=data.priorities,
            motivation=data.motivation,
            difficulties=data.difficulties,
            readiness=data.readiness,
            weekly_time=data.weekly_time,
            rules=data.rules,
            payment=data.payment,
        ),
        model=Core,
        session=session,
    )

    await publish_core_application(
        {
            "username": user.username,
            "activity": core.activity,
            "request": core.request,
            "priorities": core.priorities,
            "motivation": core.motivation,
            "difficulties": core.difficulties,
            "readiness": core.readiness,
            "weekly_time": core.weekly_time,
            "rules": core.rules,
            "payment": core.payment,
        }
    )

    return core


@router.patch("/{id}", response_model=CoreRead, status_code=status.HTTP_200_OK)
async def patch_core(
    id: int, data: CoreUpdate, session: SessionDepends
) -> Core:
    return await CRUD.patch(new_data=data, model=Core, session=session, id=id)


@router.delete("/{id}", response_model=str, status_code=status.HTTP_200_OK)
async def delete_core(id: int, session: SessionDepends) -> str:
    return await CRUD.delete(model=Core, session=session, id=id)
