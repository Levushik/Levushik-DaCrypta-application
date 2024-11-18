"""
Access and refresh tokens handling
"""

import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, Request, Response, Depends
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, schemas, models
from app.core.config import settings
from app.db.session import get_db


async def create_access_token(user_id: str,
                              data: Optional[dict] = None,
                              minutes_expire: Optional[int] = None
                              ) -> schemas.Token:
    """
    Generates JWT with data.
    TODO: why data is dict if we have AccessTokenPayload schema?
    """
    minutes_expire = minutes_expire or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = (datetime.now(timezone.utc) + timedelta(minutes=minutes_expire)).timestamp()

    payload = {} if not data else data.copy()
    payload.update(exp=expire, sub=user_id)

    return schemas.Token(
        token=jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM),
        token_type="bearer"
    )


async def create_refresh_token(db: AsyncSession, user_id: str,
                               minutes_expire: Optional[int] = None
                               ) -> schemas.Token:
    """
    Generates long-lasting single use token and puts it into db.
    """
    minutes_expire = minutes_expire or settings.REFRESH_TOKEN_EXPIRE_MINUTES
    expire = (datetime.now(timezone.utc) + timedelta(minutes=minutes_expire)).replace(tzinfo=None)

    value = secrets.token_urlsafe(settings.REFRESH_TOKEN_LENGTH_BYTES)

    await repo.refresh_token.create(
        db, obj_in=schemas.RefreshTokenInDB(refresh_token=value, user_id=user_id,
                                            expiration=expire, disposed=False))

    return schemas.Token(
        token=value,
        token_type="bearer"
    )


async def apply_access_token(token: str,
                             options: dict = None) -> \
        Optional[schemas.AccessTokenPayload]:
    """
    Checks access token and returns its data.
    Options:
        - verify_exp: True/False check for expiration
    """
    if not token:
        if options.get('verify_exp') is False:
            return None
        raise HTTPException(
            status_code=401,
            detail="Could not process access token")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.TOKEN_ALGORITHM],
                             options=options)
        token_data = schemas.AccessTokenPayload(**payload)
    except (JWTError, ValidationError) as exc:
        raise HTTPException(
            status_code=401,
            detail="Could not process access token",
        ) from exc

    user_id = token_data.sub
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Could not process access token")

    return token_data


async def apply_refresh_token(db: AsyncSession, token: str, user_id: str) -> bool:
    """
    Checks one-time refresh token
    Attempt to check disposed token will lead to invalidation of all user refresh tokens
    """
    stored_token = await repo.refresh_token.get_info_by_value(db, token)

    # attempt to use disposed token -> invalidation of all refresh tokens
    if stored_token and stored_token.disposed:
        await invalidate_refresh_tokens(db, stored_token.user_id)
        return False

    await repo.refresh_token.update(db, db_obj=stored_token, obj_in={"disposed": True})

    # incorrect or expired token
    if stored_token is None or stored_token.expiration.timestamp() <= datetime.now(
            timezone.utc).timestamp() or stored_token.user_id != user_id:
        return False

    return True


async def invalidate_refresh_tokens(db: AsyncSession, user_id: str):
    """
    Removes all user refresh tokens from database
    """
    tokens = await repo.refresh_token.get_tokens_by_user(db, user_id)
    for token in tokens:
        await repo.refresh_token.remove(db, token)


async def issue_new_token_pair(db: AsyncSession,
                               access_token: str,
                               refresh_token: str) -> schemas.TokenPair:
    """
    Validates tokens and performs refresh token rotation
    """
    token_data: schemas.AccessTokenPayload = await apply_access_token(
        access_token, {"verify_exp": False})
    user_id = token_data.sub
    tg_id = token_data.tg_id

    if user_id is None:
        raise HTTPException(status_code=401, detail="Could not process access token")

    if not await apply_refresh_token(db, refresh_token, user_id):
        raise HTTPException(status_code=401, detail="Could not process refresh token")

    new_access_token = await create_access_token(user_id, {'tg_id': tg_id})
    new_refresh_token = await create_refresh_token(db, user_id)

    return schemas.TokenPair(access_token=new_access_token,
                             refresh_token=new_refresh_token)


async def get_user(request: Request, response: Response,
                   db: AsyncSession = Depends(get_db)) -> models.User:
    """
    Validates tokens and returns current user object.
    If access token expired -> trying to obtain new one.
    """
    access_t = request.cookies.get("access_token")
    if not access_t:
        raise HTTPException(status_code=401, detail="Unauthorised")

    token_data = await apply_access_token(access_t, {'verify_exp': False})
    if token_data.exp.timestamp() > datetime.now(timezone.utc).timestamp():
        return await repo.user.get_by_id(db, token_data.sub)

    # using refresh token
    refresh_t = request.cookies.get("refresh_token")
    if not refresh_t:
        raise HTTPException(status_code=401, detail="Unauthorised")
    tokens = await issue_new_token_pair(db, access_t, refresh_t)
    response.set_cookie(key="access_token", value=tokens.access_token.token,
                        **settings.COOKIE_SETTINGS)
    response.set_cookie(key="refresh_token", value=tokens.refresh_token.token,
                        **settings.COOKIE_SETTINGS)

    return await repo.user.get_by_id(db, token_data.sub)
