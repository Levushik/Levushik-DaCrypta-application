from datetime import datetime

from pydantic import BaseModel, HttpUrl


class PriceChangePeriods(BaseModel):
    m5: float
    h1: float
    h6: float
    h24: float


class Liquidity(BaseModel):
    usd: float
    ton_pooled: float
    jetton_pooled: float


class JettonInfo(BaseModel):
    """
    Jetton basic properties.
    """
    uri: str | None
    name: str
    description: str
    image: HttpUrl
    symbol: str
    decimals: int
    amount_style: str
    render_type: str
    price: float
    pool_address: str
    address: str


class JettonExtendedInfo(BaseModel):
    """
    Jetton properties.
    """
    basic_info: JettonInfo
    market_cap: float
    liquidity: Liquidity
    volume_24h: float
    supply: float
    price_change: PriceChangePeriods

    mintable: bool
    admin_revoked: bool
    wallet_code_verified: bool
    code_verified: bool
    lp_burnt: float
    pool_created: datetime
