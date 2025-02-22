from typing import Annotated, List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from security.token import parse_access_token
from config.db import get_db_session
from models import User


def current_user(
    user_id: Annotated[str, Depends(parse_access_token)],
    session: Annotated[Session, Depends(get_db_session)],
) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def check_roles(roles: List[str], user: User, session: Session):
    """
    :param roles:
    :param user:
    :param session:
    :return:
    """
    if "admin" in roles and len(roles) == 1 and not user.is_admin:
        if not user:
            raise HTTPException(status_code=401, detail="User doesn't have permission to access this api.")
    return user


def auth(roles: List[str]):
    def wrapper(
        user: Annotated[User, Depends(current_user)],
        session: Annotated[Session, Depends(get_db_session)]
    ):
        return check_roles(roles, user, session)
    return wrapper
