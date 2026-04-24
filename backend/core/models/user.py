from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    chat_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    city: Mapped[str | None] = mapped_column(String(255), nullable=True)
    