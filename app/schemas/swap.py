"""
Swap schemas
"""

from datetime import datetime

from pydantic import BaseModel


class SwapBase(BaseModel):
    """
    Common Swap properties.
    """
    src_wallet_id: str
    token_address: str
    token_amount: float
    dex: str = "dedust"


class SwapCreate(SwapBase):
    """
    Swap request properties.
    """


class SwapUpdate(SwapBase):
    """
    Update Swap request properties.
    """


class Swap(SwapBase):
    """
    Basic schema for Swap objects
    """
    timestamp: datetime

    class Config:
        from_attributes = True
