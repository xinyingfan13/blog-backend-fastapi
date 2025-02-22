from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BaseResponse(BaseModel):
    id: UUID

    class Config:
        from_attributes = True


class SimpleResponse(BaseModel):
    status: str
    message: Optional[str] = None
