from typing import Optional, List

from pydantic import BaseModel

from schemas.base import BaseResponse
from schemas.pagination import PaginationResponse


class UserResponse(BaseResponse):
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    is_admin: bool
    activated: bool


class UpdateUserSchema(BaseModel):
    is_admin: bool
    activated: bool


class CreateUserSchema(UpdateUserSchema):
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    password: str
    phone: Optional[str]


class UserListResponse(PaginationResponse):
    items: List[UserResponse]
