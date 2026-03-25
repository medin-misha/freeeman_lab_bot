from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.user import UserCreate, UserRead, UserUpdate
from core import database
from core.models import User
from service import CRUD

router = APIRouter(
    tags=["users"], prefix="/users",
)
SessionDepends = Annotated[AsyncSession, Depends(database.get_session)]


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, session: SessionDepends) -> User:
    return await CRUD.create(data=data, model=User, session=session)


@router.get("", response_model=list[UserRead], status_code=status.HTTP_200_OK)
async def get_users(
    session: SessionDepends,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    search: str | None = None,
    field: str | None = None,
) -> list[User]:
    return await CRUD.get(
        model=User,
        session=session,
        page=page,
        limit=limit,
        search=search,
        field=field,
    )


@router.get("/{id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user(id: int, session: SessionDepends) -> User:
    return await CRUD.get(model=User, session=session, id=id)


@router.patch("/{id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def patch_user(id: int, data: UserUpdate, session: SessionDepends) -> User:
    return await CRUD.patch(new_data=data, model=User, session=session, id=id)


@router.delete("/{id}", response_model=str, status_code=status.HTTP_200_OK)
async def delete_user(id: int, session: SessionDepends) -> str:
    return await CRUD.delete(model=User, session=session, id=id)
