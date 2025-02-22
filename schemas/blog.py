from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from schemas.as_form import as_form
from schemas.base import BaseResponse
from schemas.pagination import PaginationResponse


@as_form
class CreateBlogSchema(BaseModel):
    title: str
    description: str


@as_form
class UpdateBlogSchema(CreateBlogSchema):
    title: Optional[str] = None
    description: Optional[str] = None


class BlogResponse(BaseResponse, CreateBlogSchema):
    image: str
    created_at: datetime
    updated_at: datetime


class BlogListResponse(PaginationResponse):
    items: List[BlogResponse]

