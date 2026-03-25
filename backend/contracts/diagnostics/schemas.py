from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from core.models.diagnostics import DiagnosticStatus


class DiagnosticStatusEnum(str, Enum):
    PENDING = DiagnosticStatus.PENDING
    IN_PROGRESS = DiagnosticStatus.IN_PROGRESS
    COMPLETED = DiagnosticStatus.COMPLETED


class DiagnosticsBase(BaseModel):
    status: DiagnosticStatusEnum | None = None
    file_id: int | None = None
    result_file_id: int | None = None
    passed_at: datetime | None = None
    user_id: int | None = None


class DiagnosticsCreate(BaseModel):
    status: DiagnosticStatusEnum = DiagnosticStatusEnum.PENDING
    file_id: int
    result_file_id: int | None = None
    passed_at: datetime | None = None
    user_id: int


class DiagnosticsUpdate(DiagnosticsBase):
    pass


class DiagnosticsRead(DiagnosticsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: DiagnosticStatusEnum
    file_id: int
    user_id: int
