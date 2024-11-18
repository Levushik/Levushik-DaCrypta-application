from dexscreener import DexscreenerClient
from pytoncenter import get_client
from pytoncenter.v3.models import *

from app.core.config import settings
from app.schemas.jetton import JettonExtendedInfo, JettonInfo, PriceChangePeriods, Liquidity

jetton_hashes_verified = [
    "BXGXbGPsG3VQIwomCdvts24bZO+NAioWs06lcGMYWy8=",
    "eN3/T29/AAAAAAAAAAAAAKdg1inVND520EUBfZ3CFvw="
]
jetton_wallet_hashes_verified = [
    "p2DWKdU0PnbQRQF9ncIW/IoweoN3gV/rKwpcSQ5zNIY="
]

NULL_ADDRESS = "EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c"

client_toncenter = get_client(version="v3", network="mainnet", api_key=settings.TONCENTER_API_KEY)
dex_client = DexscreenerClient()


async def get_jetton_info(jetton_addr: str) -> JettonExtendedInfo:
    pair = dex_client.get_token_pairs(jetton_addr)[0]

    price = pair.price_usd
    market_cap = pair.fdv
    liquidity = pair.liquidity.usd
    ton_pooled = pair.liquidity.quote
    jetton_pooled = pair.liquidity.base
    volume_24h = pair.volume.h24
    lp_addr = pair.pair_address

    jetton_masters = await client_toncenter.get_jetton_masters(
        GetJettonMastersRequest(address=jetton_addr))
    lp_masters = await client_toncenter.get_jetton_masters(GetJettonMastersRequest(address=lp_addr))
    lp_supply = lp_masters[0].total_supply
    lp_burnt_wallet = await client_toncenter.get_jetton_wallets(
        GetJettonWalletsRequest(owner_address=NULL_ADDRESS, jetton_address=lp_addr)
    )
    if lp_burnt_wallet:
        lp_burnt = lp_burnt_wallet[0].balance
    else:
        lp_burnt = 0

    lp_burnt_percent = lp_burnt / lp_supply

    jetton_info = jetton_masters[0]

    supply = jetton_info.total_supply / 1e9
    mintable = jetton_info.mintable
    admin_revoked = jetton_info.admin_address == NULL_ADDRESS

    jetton_wallet_code_verified = jetton_info.jetton_wallet_code_hash in jetton_wallet_hashes_verified
    jetton_code_verified = jetton_info.code_hash in jetton_hashes_verified

    info = JettonExtendedInfo(
        basic_info=JettonInfo(
            price=price,
            uri=jetton_info.jetton_content.uri,
            name=jetton_info.jetton_content.name,
            description=jetton_info.jetton_content.description,
            image=jetton_info.jetton_content.image,
            symbol=jetton_info.jetton_content.symbol,
            decimals=jetton_info.jetton_content.decimals,
            amount_style=jetton_info.jetton_content.amount_style,
            render_type=jetton_info.jetton_content.render_type,
            pool_address=pair.pair_address,
            address=jetton_addr
        ),
        market_cap=market_cap,
        liquidity=Liquidity(
            usd=liquidity,
            ton_pooled=ton_pooled,
            jetton_pooled=jetton_pooled
        ),
        volume_24h=volume_24h,
        supply=supply,
        price_change=PriceChangePeriods(
            **pair.price_change.dict()
        ),

        mintable=mintable,
        admin_revoked=admin_revoked,
        wallet_code_verified=jetton_wallet_code_verified,
        code_verified=jetton_code_verified,
        lp_burnt=lp_burnt_percent,
        pool_created=pair.pair_created_at
    )
    return info

# if __name__ == "__main__":
#     asyncio.run(get_jetton_info("EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE"))
