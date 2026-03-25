from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str | None = None
    email: str | None = None
    phone: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(UserBase):
    chat_id: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    phone: str | None = None
    chat_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chat_id: str
