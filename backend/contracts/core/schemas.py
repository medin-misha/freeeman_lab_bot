from datetime import date

from pydantic import BaseModel, ConfigDict


class CoreFormSubmit(BaseModel):
    telegram_id: str
    full_name: str
    birth_date: date
    city: str
    activity: str | None = None
    request: str | None = None
    priorities: list[str] | None = None
    motivation: str | None = None
    difficulties: str | None = None
    readiness: str | None = None
    weekly_time: str | None = None
    rules: str | None = None
    payment: str | None = None


class CoreCreate(BaseModel):
    user_id: int
    activity: str | None = None
    request: str | None = None
    priorities: list[str] | None = None
    motivation: str | None = None
    difficulties: str | None = None
    readiness: str | None = None
    weekly_time: str | None = None
    rules: str | None = None
    payment: str | None = None


class CoreUpdate(BaseModel):
    activity: str | None = None
    request: str | None = None
    priorities: list[str] | None = None
    motivation: str | None = None
    difficulties: str | None = None
    readiness: str | None = None
    weekly_time: str | None = None
    rules: str | None = None
    payment: str | None = None
    user_id: int | None = None


class CoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    activity: str | None = None
    request: str | None = None
    priorities: list[str] | None = None
    motivation: str | None = None
    difficulties: str | None = None
    readiness: str | None = None
    weekly_time: str | None = None
    rules: str | None = None
    payment: str | None = None
