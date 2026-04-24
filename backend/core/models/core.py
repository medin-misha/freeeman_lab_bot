from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Core(Base):
    activity: Mapped[str | None] = mapped_column(Text, nullable=True)
    request: Mapped[str | None] = mapped_column(Text, nullable=True)
    priorities: Mapped[list | None] = mapped_column(JSON, nullable=True)
    motivation: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulties: Mapped[str | None] = mapped_column(Text, nullable=True)
    readiness: Mapped[str | None] = mapped_column(String(255), nullable=True)
    weekly_time: Mapped[str | None] = mapped_column(String(255), nullable=True)
    rules: Mapped[str | None] = mapped_column(String(255), nullable=True)
    payment: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
