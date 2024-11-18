"""
Telegram auth schemas
"""

from typing import Optional

from pydantic import BaseModel, HttpUrl


class TgAuthorizationData(BaseModel):
    """
    Data returned by telegram from login
    """
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[HttpUrl] = None
    auth_date: int
    hash: str

    def __str__(self):
        """
        data-check-string. Concatenation of all received fields `key=value` in alphabetical order.
        Reference: https://core.telegram.org/widgets/login#checking-authorization
        """
        res = sorted(
            f'{x[0]}={x[1]}'
            for x in self.__dict__.items()
            if x[0] != 'hash' and x[1] is not None
        )
        return '\n'.join(res)


class TgAuthorisationResult(BaseModel):
    """
    Result of validating TgAuthorisationData
    """
    result: bool
    admin: bool
