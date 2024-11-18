"""
Wallet data operations
"""

from typing import Any, Optional, Iterable

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.repo.default import CRUDBase


class WalletRepo(CRUDBase[models.Wallet, schemas.WalletCreate, schemas.WalletUpdate]):
    """
    Data operations for wallets
    """

    async def get_by_id(self, db: AsyncSession, obj_id: Any) -> Optional[models.Wallet]:
        """
        Get object by id
        None if nothing found or object disposed
        """
        res = await db.scalar(select(self.model)
                              .filter(and_(self.model.id == obj_id,
                                           self.model.disposed == False))
                              .limit(1))
        return res

    async def get_user_wallets(self, db: AsyncSession, user_id: str) -> Iterable[models.Wallet]:
        """
        Get all wallets that belong to user
        """
        res = await db.scalars(select(self.model)
                               .filter(and_(self.model.owner_id == user_id,
                                            self.model.disposed == False)))
        return res.all()


wallet = WalletRepo(models.Wallet)
