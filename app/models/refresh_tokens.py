"""
SQLAlchemy refresh token model
"""
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class RefreshToken(Base):
    """
    Stored single use tokens
    """
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(autoincrement=True, default=0)
    refresh_token: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(index=True)
    expiration: Mapped[datetime]
    disposed: Mapped[bool]
