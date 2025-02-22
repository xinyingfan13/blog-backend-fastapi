from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from config.db import get_db_session
from services.blog import BlogService
from services.base import BaseService
from services.user import UserService


class Core(BaseService):
    """Core service for the application."""

    def __init__(self, session: Session):
        super(Core, self).__init__(session)
        self.user = UserService(session)
        self.blog = BlogService(session)


def core_services(session: Annotated[Session, Depends(get_db_session)]) -> Core:
    return Core(session)
