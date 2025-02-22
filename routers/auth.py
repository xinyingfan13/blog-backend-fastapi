from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from config.setting import settings
from models import User
from schemas.auth import Token, AuthSchema, UpdatePasswordSchema
from schemas.base import SimpleResponse
from schemas.user import UserResponse
from security.auth import current_user
from security.token import create_access_token
from services.core import Core, core_services

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=Token)
def login(data: AuthSchema,  core: Annotated[Core, Depends(core_services)]) -> Token:
    user: User = core.user.get_user_by_email(data.email)
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    if not user:
        raise exception
    if not user.verify_password(data.password):
        raise exception
    access_token_expires = timedelta(minutes=settings.jwt_default_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/update-password", response_model=SimpleResponse)
def update_password(
    data: UpdatePasswordSchema,
    user: Annotated[User, Depends(current_user)],
) -> SimpleResponse:
    if not user.verify_password(data.old_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password",
        )
    user.set_password(data.new_password)
    return SimpleResponse(status="success", message="Password has been updated.")


@router.get("/me", response_model=UserResponse)
def get_me(user: Annotated[User, Depends(current_user)]):
    return user

