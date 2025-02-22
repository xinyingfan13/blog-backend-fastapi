from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from passlib.context import CryptContext

from models.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    firstname: Mapped[str] = mapped_column(String(32), nullable=True)
    lastname: Mapped[str] = mapped_column(String(32), nullable=True)
    email: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    activated: Mapped[bool] = mapped_column(Boolean, default=True)

    def verify_password(self, plain_password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, pwd: str):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.password = pwd_context.hash(pwd)
