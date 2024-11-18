"""
Telegram login handling
"""

import hashlib
import hmac
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import repo, schemas
from app.core.config import settings
from app.services.security.ar_tokens import create_access_token, create_refresh_token


def check_tg_credentials(
        tg_credentials: schemas.TgAuthorizationData) -> schemas.TgAuthorisationResult:
    """
    Confirms that telegram credentials are recent and actually sent by telegram.
    """
    data_check_string = bytes(str(tg_credentials), 'utf-8')

    if not settings.DEBUG and datetime.now().timestamp() - tg_credentials.auth_date >= 1 * 60:
        return schemas.TgAuthorisationResult(result=False, admin=False)

    key_user = hashlib.sha256(settings.USER_BOT_TOKEN.encode('utf-8')).digest()

    secret_user = hmac.new(key_user, data_check_string, hashlib.sha256).hexdigest()

    is_admin = False
    is_valid = tg_credentials.hash == secret_user

    return schemas.TgAuthorisationResult(result=is_valid, admin=is_admin)


async def login_via_tg(db: AsyncSession,
                       tg_data: schemas.TgAuthorizationData) -> schemas.TokenPair:
    """
    Returns token pair on successful login through telegram
    """
    check = check_tg_credentials(tg_data)

    if not check.result:
        raise HTTPException(status_code=401, detail='Unauthorised')

    user_id = str(tg_data.id)
    data = {'tg_id': user_id}

    user = await repo.user.get_by_id(db, user_id)
    if user is None:
        user = schemas.UserCreate(id=user_id, username=tg_data.username,
                                  name=tg_data.first_name, surname=tg_data.last_name,
                                  photo_url=str(tg_data.photo_url))
        await repo.user.create(db, user)
    else:
        user_update = schemas.UserUpdate(username=tg_data.username,
                                         name=tg_data.first_name, surname=tg_data.last_name,
                                         photo_url=str(tg_data.photo_url))
        await repo.user.update(db, db_obj=user, obj_in=user_update)

    access_token = await create_access_token(user_id, data)
    refresh_token = await create_refresh_token(db, user_id)

    return schemas.TokenPair(access_token=access_token,
                             refresh_token=refresh_token)
