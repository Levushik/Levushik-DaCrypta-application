"""
Token data operations
"""

from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_tokens import RefreshToken
from app.repo.default import CRUDBase


class RefreshTokenRepo(CRUDBase[RefreshToken, RefreshToken, RefreshToken]):
    """
    Data operations for refresh tokens
    """

    async def get_tokens_by_user(self, db: AsyncSession, user_id: str) -> Iterable[RefreshToken]:
        """
        Get all stored tokens issued for specified user
        """
        res = await db.scalars(select(self.model).filter(self.model.user_id == user_id))
        return res.all()

    async def get_info_by_value(self, db: AsyncSession, token: str) -> RefreshToken:
        """
        Get stored information about token by its value
        """
        return await db.scalar(select(self.model).filter(self.model.refresh_token == token))

    async def remove(self, db: AsyncSession, token: RefreshToken):
        """
        Removes stored token from DB by value
        """
        await db.delete(token)
        await db.commit()


refresh_token = RefreshTokenRepo(RefreshToken)
