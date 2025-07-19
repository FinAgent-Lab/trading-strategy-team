from src.dtos.kis.tradeDto import TradeDto
from langchain_core.tools import tool
from src.services.kis import KisService

kis_service = KisService()


@tool
async def get_access_token(
    user_id: str,
) -> str:
    """
    # Get access token
    """

    return await kis_service.get_access_token(user_id)


@tool
async def update_access_token(
    user_id: str,
) -> str:
    """
    # Update access token
    If the access token is expired or occured error because of access token, you can update it by calling this tool.
    """

    return await kis_service.update_access_token(user_id)


@tool
async def get_overseas_stock_daily_price(
    input: TradeDto.GetOverseasStockDailyPriceInput,
) -> TradeDto.GetOverseasStockDailyPriceOutput:
    """
    # Get periodical market price of foreign stocks
    You can get a periodical market price of foreign stocks.
    """

    return await kis_service.get_overseas_stock_daily_price(input)


@tool
async def order_overseas_stock(
    input: TradeDto.OrderOverseasStockInput,
) -> TradeDto.OrderOverseasStockOutput:
    """
    # Order foreign stocks
    """

    return await kis_service.order_overseas_stock(input)


@tool
async def book_overseas_stock_order(
    input: TradeDto.BookOverseasStockOrderInput,
) -> TradeDto.BookOverseasStockOrderOutput:
    """
    # Book foreign stocks
    """

    return await kis_service.book_overseas_stock_order(input)


@tool
async def cancel_overseas_stock_order(
    input: TradeDto.CancelOverseasStockOrderInput,
) -> dict:
    """
    # Cancel foreign stocks
    """

    return await kis_service.cancel_overseas_stock_order(input)


@tool
async def get_overseas_stock_order_resv_list(
    input: TradeDto.GetOverseasStockOrderResvListInput,
) -> dict:
    """
    # Get foreign stock order reservation list
    """

    return await kis_service.get_overseas_stock_order_resv_list(input)
