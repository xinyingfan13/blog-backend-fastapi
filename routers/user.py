import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from models import User
from schemas.base import SimpleResponse
from schemas.user import CreateUserSchema, UserResponse, UpdateUserSchema, UserListResponse
from security.auth import auth, current_user
from services.core import Core, core_services

router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[],
)


@router.post("/create", response_model=UserResponse)
def create_user(
    data: CreateUserSchema,
    _: Annotated[User, Depends(auth(["admin"]))],
    core: Annotated[Core, Depends(core_services)],
) -> UserResponse:
    check_user = core.get_item_by_filter(User, {"email": data.email})
    if check_user and not check_user.activated:
        check_user.activated = True
        return check_user
    elif check_user and check_user.activated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User exists.")

    user = core.get_or_create(User, {**data.dict()})
    user.set_password(data.password)
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: uuid.UUID,
    data: UpdateUserSchema,
    _: Annotated[User, Depends(auth(["admin"]))],
    core: Annotated[Core, Depends(core_services)],
) -> UserResponse:
    user = core.get_or_not_found(User, user_id)
    user.is_admin = data.is_admin
    user.activated = user.activated
    return user


@router.get("/list", response_model=UserListResponse)
def get_users(
    user: Annotated[User, Depends(current_user)],
    core: Annotated[Core, Depends(core_services)],
) -> UserListResponse:
    users = core.user.get_all(user.is_admin)
    return UserListResponse(total=len(users), items=users)


@router.delete("/{user_id}", response_model=SimpleResponse)
def delete_user(
    user_id: uuid.UUID,
    _: Annotated[User, Depends(auth(["admin"]))],
    core: Annotated[Core, Depends(core_services)],
) -> SimpleResponse:
    user = core.get_or_not_found(User, user_id)
    user.activated = False
    return SimpleResponse(statis="success", message="User is deactivated")
