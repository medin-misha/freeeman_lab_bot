from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class DiagnosticStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    
    

class Diagnostics(Base):
    status: Mapped[str] = mapped_column(String(32), default=DiagnosticStatus.PENDING)
    file_id: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=False)
    result_file_id: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=True)
    passed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
