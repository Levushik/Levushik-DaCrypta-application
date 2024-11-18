"""
v1 routes
"""

from fastapi import APIRouter

from app.web_api.v1 import auth
from app.web_api.v1 import jetton
from app.web_api.v1 import swap
from app.web_api.v1 import wallet

v1_router = APIRouter()
v1_router.include_router(swap.router, tags=['Swap'])
v1_router.include_router(auth.router, tags=['Auth'])
v1_router.include_router(jetton.router, tags=['Jetton'])
v1_router.include_router(wallet.router, tags=['Wallet'])
