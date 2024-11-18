"""
SQLAlchemy client user model
"""
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """
    Regular user
    """
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(nullable=True)

    name: Mapped[str] = mapped_column(nullable=True)
    surname: Mapped[str] = mapped_column(nullable=True)

    photo_url: Mapped[str] = mapped_column(nullable=True)

    # pylint: disable=not-callable
    created: Mapped[datetime] = mapped_column(server_default=func.now())
