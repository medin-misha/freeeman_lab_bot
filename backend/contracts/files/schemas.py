from pydantic import BaseModel
from fastapi import UploadFile
from datetime import datetime

class FileBase(BaseModel):
    link: str

class FileCreate(FileBase):
    pass

class FileUpload(BaseModel):
    file: UploadFile

    class Config:
        arbitrary_types_allowed = True

class FileReturn(FileBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True