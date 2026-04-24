from datetime import date

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str | None = None
    email: str | None = None
    phone: str | None = None
    full_name: str | None = None
    birth_date: date | None = None
    city: str | None = None


class UserCreate(UserBase):
    chat_id: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    phone: str | None = None
    chat_id: str | None = None
    full_name: str | None = None
    birth_date: date | None = None
    city: str | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chat_id: str
