from fastapi import APIRouter, Depends
from pytoniq import LiteBalancer, WalletV4R2
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app import schemas
from app import services
from app.db.session import get_db

router = APIRouter(prefix='/swap')


@router.post("/swap_to_jetton")
async def swap_to_jetton(swap_info: schemas.SwapCreate,
                         user: models.User = Depends(services.security.get_user),
                         db: AsyncSession = Depends(get_db)):
    """
    Swap TON with some token on dedust.
    """
    wallet = await services.wallet.get_wallet(swap_info.src_wallet_id, user.id, db)
    ton_wallet = wallet.mnemonics

    mnemonics = ton_wallet.replace(',', ' ').split()
    client = LiteBalancer.from_mainnet_config(trust_level=1)
    await client.start_up()
    wallet = await WalletV4R2.from_mnemonic(mnemonics=mnemonics, provider=client)

    if swap_info.dex == "dedust":
        swapper = services.dedust_swapper.DedustSwapper
    elif swap_info.dex == "stonfi":
        swapper = services.stonfi_swapper.StonfiSwapper
    else:
        raise ValueError(f"Unknown dex: {swap_info.dex}")

    await swapper.swap_to_jetton(wallet, swap_info.token_address, swap_info.token_amount)

    return True


@router.post("/swap_to_native")
async def swap_to_native(swap_info: schemas.SwapCreate,
                         user: models.User = Depends(services.security.get_user),
                         db: AsyncSession = Depends(get_db)):
    """
    Swap TON with some token on dedust.
    """
    wallet = await services.wallet.get_wallet(swap_info.src_wallet_id, user.id, db)
    ton_wallet = wallet.mnemonics

    mnemonics = ton_wallet.replace(',', ' ').split()
    client = LiteBalancer.from_mainnet_config(trust_level=1)
    await client.start_up()
    wallet = await WalletV4R2.from_mnemonic(mnemonics=mnemonics, provider=client)

    if swap_info.dex == "dedust":
        swapper = services.dedust_swapper.DedustSwapper
    elif swap_info.dex == "stonfi":
        swapper = services.stonfi_swapper.StonfiSwapper
    else:
        raise ValueError(f"Unknown dex: {swap_info.dex}")

    await swapper.swap_to_native(wallet, swap_info.token_address, swap_info.token_amount)

    return True
