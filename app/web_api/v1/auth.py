"""
Endpoints for authentication
"""
from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, services, models
from app.core.config import settings
from app.db.session import get_db

router = APIRouter(prefix='/auth')


@router.post("/login_tg")
async def login_tg(response: Response,
                   creds: schemas.TgAuthorizationData,
                   db: AsyncSession = Depends(get_db)):
    """
    User login, creates access and refresh tokens
    """
    tokens = await services.security.login_via_tg(db, creds)

    response.set_cookie(key="access_token", value=tokens.access_token.token,
                        **settings.COOKIE_SETTINGS)
    response.set_cookie(key="refresh_token", value=tokens.refresh_token.token,
                        **settings.COOKIE_SETTINGS)

    return True


@router.post("/logout")
async def logout(request: Request, response: Response,
                 db: AsyncSession = Depends(get_db)):
    """
    Logs user out by deleting cookies and invalidating refresh token
    """
    access = request.cookies.get("access_token")
    refresh = request.cookies.get("refresh_token")

    response.delete_cookie(key="access_token", **settings.COOKIE_SETTINGS)
    response.delete_cookie(key="refresh_token", **settings.COOKIE_SETTINGS)

    if not access:
        return

    try:
        token_data = await services.security.apply_access_token(access, {'verify_exp': False})
        await services.security.apply_refresh_token(db, refresh, token_data.sub)
    except Exception as exc:
        pass  # tokens must be cleared in any case


@router.get("/me", response_model=schemas.User)
async def get_logged_user_info(
        user: models.User = Depends(services.security.get_user)):
    return user
