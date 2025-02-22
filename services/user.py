from typing import Optional

from models import User
from services.base import BaseService


class UserService(BaseService):
    def get_user_by_email(self, email: str) -> Optional[User]:
        result = self.session.query(User).where(User.email == email).first()
        return result

    def get_all(self, is_admin: bool):
        query = self.session.query(User)
        if not is_admin:
            query.where(User.is_admin.is_(False))
        return query.all()
