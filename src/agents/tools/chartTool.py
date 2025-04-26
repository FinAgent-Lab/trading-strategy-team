from src.dtos.kis.tradeDto import TradeDto
from langchain_core.tools import tool
from src.services.kis import KisService

kis_service = KisService()

@tool
def get_overseas_stock_daily_price(
    input: TradeDto.GetOverseasStockDailyPriceInput,
) -> TradeDto.GetOverseasStockDailyPriceOutput:
    """해외 주식의 일별 시세를 조회합니다."""
    return kis_service.get_overseas_stock_daily_price(input)
