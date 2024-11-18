from typing import Iterable

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, services, schemas, models


async def create_wallet(data: schemas.WalletCreate, user_id: str,
                        db: AsyncSession) -> models.Wallet:
    data_enriched = schemas.WalletCreateInternal(**data.model_dump(), owner_id=user_id)
    return await repo.wallet.create(db, obj_in=data_enriched)


async def get_wallet(wallet_id: str, user_id: str, db: AsyncSession) -> models.Wallet:
    wallet = await repo.wallet.get_by_id(db, wallet_id)

    if wallet is None or wallet.owner_id != user_id:
        raise HTTPException(status_code=404, detail='Wallet not found')

    return wallet


async def get_funds(wallet_id: str, user_id: str, db: AsyncSession) -> schemas.WalletFunds:
    wallet = await get_wallet(wallet_id, user_id, db)

    return await services.wallet_funds.get_wallet_funds(wallet.address)


async def get_all_wallets(user_id: str, db: AsyncSession) -> Iterable[models.Wallet]:
    return await repo.wallet.get_user_wallets(db, user_id)


async def update_wallet(wallet_id: str, user_id: str, data: schemas.WalletUpdate,
                        db: AsyncSession) -> bool:
    wallet = await get_wallet(wallet_id, user_id, db)

    await repo.wallet.update(db, db_obj=wallet, obj_in=data)

    return True


async def delete_wallet(wallet_id: str, user_id: str, db: AsyncSession) -> bool:
    await get_wallet(wallet_id, user_id, db)

    await repo.wallet.remove_by_id(db, obj_id=wallet_id)

    return True
