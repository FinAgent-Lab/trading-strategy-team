from fastapi import APIRouter, Depends

from src.services.kis import KisService

kis_router = router = APIRouter(prefix="/kis")


@router.get("/access-token")
async def get_access_token(
    kis_service: KisService = Depends(lambda: KisService()),
):
    return kis_service.get_access_token()
