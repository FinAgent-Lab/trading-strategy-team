from src.dtos.kis.tradeDto import TradeDto
from langchain_core.tools import tool
from src.services.kis import KisService

kis_service = KisService()


@tool
def get_overseas_stock_daily_price(
    input: TradeDto.GetOverseasStockDailyPriceInput,
) -> TradeDto.GetOverseasStockDailyPriceOutput:
    """
    # Get periodical market price of foreign stocks
    You can get a periodical market price of foreign stocks.
    """

    return kis_service.get_overseas_stock_daily_price(input)


@tool
def order_overseas_stock(
    input: TradeDto.OrderOverseasStockInput,
    is_buy: bool,
) -> TradeDto.OrderOverseasStockOutput:
    """
    # Order foreign stocks
    """

    return kis_service.order_overseas_stock(input, is_buy)


@tool
def book_overseas_stock_order(
    input: TradeDto.BookOverseasStockOrderInput,
    is_buy: bool,
) -> TradeDto.BookOverseasStockOrderOutput:
    """
    # Book foreign stocks
    """

    return kis_service.book_overseas_stock_order(input, is_buy)


@tool
def cancel_overseas_stock_order(
    input: TradeDto.CancelOverseasStockOrderInput,
) -> dict:
    """
    # Cancel foreign stocks
    """

    return kis_service.cancel_overseas_stock_order(input)


@tool
def get_overseas_stock_order_resv_list(
    input: TradeDto.GetOverseasStockOrderResvListInput,
) -> dict:
    """
    # Get foreign stock order reservation list
    """

    return kis_service.get_overseas_stock_order_resv_list(input)
