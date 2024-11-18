from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app import services
from app.db.session import get_db

router = APIRouter(prefix='/wallet')


@router.get("/{wallet_id}/get_funds", response_model=schemas.WalletFunds)
async def get_wallet_funds(wallet_id: str,
                           user: models.User = Depends(services.security.get_user),
                           db: AsyncSession = Depends(get_db)):
    """
    Get funds present on wallet.
    """
    return await services.wallet.get_funds(wallet_id, user.id, db)


@router.post("/", status_code=201)
async def create_wallet(data: schemas.WalletCreate,
                        user: models.User = Depends(services.security.get_user),
                        db: AsyncSession = Depends(get_db)) -> str:
    wallet = await services.wallet.create_wallet(data, user.id, db)
    return str(wallet.id)


@router.get("/all", response_model=List[schemas.Wallet])
async def get_all_user_wallets(user: models.User = Depends(services.security.get_user),
                               db: AsyncSession = Depends(get_db)):
    """
    Get all wallets belonging to user
    """
    return await services.wallet.get_all_wallets(user.id, db)


@router.get("/{wallet_id}", response_model=schemas.Wallet)
async def get_wallet(wallet_id: str,
                     user: models.User = Depends(services.security.get_user),
                     db: AsyncSession = Depends(get_db)):
    return await services.wallet.get_wallet(wallet_id, user.id, db)


@router.put("/{wallet_id}")
async def update_wallet(wallet_id: str,
                        data: schemas.WalletUpdate,
                        user: models.User = Depends(services.security.get_user),
                        db: AsyncSession = Depends(get_db)) -> bool:
    return await services.wallet.update_wallet(wallet_id, user.id, data, db)


@router.delete("/{wallet_id}")
async def delete_wallet(wallet_id: str,
                        user: models.User = Depends(services.security.get_user),
                        db: AsyncSession = Depends(get_db)) -> bool:
    return await services.wallet.delete_wallet(wallet_id, user.id, db)
