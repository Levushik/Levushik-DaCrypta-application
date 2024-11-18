from fastapi import APIRouter, Depends

from app import models, schemas
from app import services

router = APIRouter(prefix='/jetton')


@router.get("/info", response_model=schemas.JettonExtendedInfo)
async def get_jetton_info(jetton_addr: str,
                          user: models.User = Depends(services.security.get_user)):
    """
    Get jetton info.
    """
    return services.jetton_analyzer.get_jetton_info(jetton_addr)
