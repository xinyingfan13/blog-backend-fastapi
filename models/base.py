import uuid
from datetime import datetime

from sqlalchemy import DateTime, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, class_mapper


class Model(DeclarativeBase):
    pass


class BaseModel(Model):
    __abstract__ = True

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """
        Converts an SQLAlchemy model instance to a dictionary, excluding internal SQLAlchemy attributes.
        """
        # Use class_mapper to get the columns
        return {column.name: getattr(self, column.name) for column in class_mapper(self.__class__).columns}

