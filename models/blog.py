from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel

if TYPE_CHECKING:
    from models import User


class Blog(BaseModel):
    __tablename__ = "blog"

    title: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(String(800), nullable=False, unique=True)
    image: Mapped[str] = mapped_column(String(500), nullable=False)

    author_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    author: Mapped["User"] = relationship("User")
