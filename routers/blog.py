import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File

from models import User, Blog
from schemas.base import SimpleResponse
from schemas.blog import CreateBlogSchema, BlogResponse, BlogListResponse, UpdateBlogSchema
from security.auth import auth
from services.core import Core, core_services

router = APIRouter(
    prefix="/blogs",
    tags=["Blog"],
    dependencies=[],
)


@router.get("/list", response_model=BlogListResponse)
def get_blog_list(
    core: Annotated[Core, Depends(core_services)],
) -> BlogListResponse:
    items = core.blog.get_all_blogs()
    return BlogListResponse(items=items, total=len(items))


@router.post("/create", response_model=BlogResponse)
def create_blog(
    file: UploadFile,
    data: Annotated[CreateBlogSchema, Depends(CreateBlogSchema.as_form)],
    current_user: Annotated[User, Depends(auth(["admin"]))],
    core: Annotated[Core, Depends(core_services)],
) -> BlogResponse:
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed.",
        )
    image = core.blog.save_image(file=file)
    blog = core.get_or_create(Blog, {**data.dict(), "author_id": current_user.id, "image": image})
    return blog


@router.put("/{blog_id}", response_model=BlogResponse)
def update_blog(
    blog_id: uuid.UUID,
    data: Annotated[UpdateBlogSchema, Depends(UpdateBlogSchema.as_form)],
    _: Annotated[User, Depends(auth(["admin"]))],
    core: Annotated[Core, Depends(core_services)],
    file: Optional[UploadFile] = File(None),
) -> BlogResponse:
    blog = core.get_or_not_found(Blog, blog_id)
    if file and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed.",
        )
    image = blog.image
    if file:
        core.blog.remove_old_image(blog.image)
        image = core.blog.save_image(file=file)
    blog = core.update_or_not_found(Blog, blog_id, {**data.dict(), "image": image})
    return blog


@router.get("/{blog_id}", response_model=BlogResponse)
def get_blog(
    blog_id: uuid.UUID,
    _: Annotated[User, Depends(auth(["admin"]))],
    core: Annotated[Core, Depends(core_services)],
) -> BlogResponse:
    item = core.get_or_not_found(Blog, blog_id)
    return item


@router.delete("/{blog_id}", response_model=SimpleResponse)
def delete_blog(
    blog_id: uuid.UUID,
    _: Annotated[User, Depends(auth(["admin"]))],
    core: Annotated[Core, Depends(core_services)],
) -> SimpleResponse:
    blog = core.get_or_not_found(Blog, blog_id)
    core.blog.delete_blog(blog.id)
    return SimpleResponse(status="success", message="Blog is deleted.")
