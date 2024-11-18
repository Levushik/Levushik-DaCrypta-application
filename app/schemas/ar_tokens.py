"""
Token schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AccessTokenPayload(BaseModel):
    """
    Data included in access token
    """
    exp: datetime
    sub: Optional[str] = None
    tg_id: Optional[str] = None


class Token(BaseModel):
    """
    Response with token and its type
    """
    token: str
    token_type: str


class RefreshTokenInDB(BaseModel):
    """
    Refresh token format in DB
    """
    refresh_token: str
    expiration: datetime
    user_id: str
    disposed: bool


class TokenPair(BaseModel):
    """
    Concatenation of Access and Refresh tokens
    """
    access_token: Token
    refresh_token: Token
