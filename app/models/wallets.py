"""
SQLAlchemy wallet model
"""
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Wallet(Base):
    """
    TON wallet
    """
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),
                                          index=True)

    name: Mapped[str]
    mnemonics: Mapped[str]
    address: Mapped[str]

    disposed: Mapped[bool] = mapped_column(default=False)

    # pylint: disable=not-callable
    created: Mapped[datetime] = mapped_column(server_default=func.now())
