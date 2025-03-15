from fastapi import APIRouter, Depends

from src.dtos.kis.tradeDto import TradeDto
from src.services.kis import KisService

kis_router = router = APIRouter(prefix="/kis")


@router.get("/access-token")
async def get_access_token(
    kis_service: KisService = Depends(lambda: KisService()),
):
    return kis_service.get_access_token()


@router.post(
    "/foreign-stock/daily-price",
    tags=["해외 주식"],
    summary="해외 주식 기간별 시세",
)
async def get_overseas_stock_daily_price(
    access_token: str,
    input: TradeDto.GetOverseasStockDailyPriceInputDto,
    kis_service: KisService = Depends(lambda: KisService()),
):
    return kis_service.get_overseas_stock_daily_price(access_token, input)


@router.post(
    "/foreign-stock/order",
    tags=["해외 주식"],
    summary="해외 주식 주문",
)
async def order_foreign_stock(
    access_token: str,
    input: TradeDto.OrderOverseasStockInputDto,
    isBuy: bool,
    kis_service: KisService = Depends(lambda: KisService()),
):
    return kis_service.order_overseas_stock(access_token, input, isBuy)


@router.post(
    "/foreign-stock/book",
    tags=["해외 주식"],
    summary="해외 주식 주문 예약",
)
async def book_foreign_stock_order(
    access_token: str,
    input: TradeDto.BookOverseasStockOrderInputDto,
    isBuy: bool,
    kis_service: KisService = Depends(lambda: KisService()),
):
    return kis_service.book_overseas_stock_order(access_token, input, isBuy)
