from fastapi import APIRouter, Depends
from src.services.practice import PracticeService
from src.dtos.tradingAgent.chatDto import TradingAgentChatDto
from src.services.tradingAgent import TradingAgentService

agent_router = router = APIRouter(prefix="/agent")


@router.post("/trading/chat")
async def chat_trading_agent(
    input: TradingAgentChatDto,
    trading_agent_service: TradingAgentService = Depends(lambda: TradingAgentService()),
):
    return trading_agent_service.chat_trading_agent(input.message)


@router.post("/practice/chat", tags=["practice"])
async def chat_practice_agent(
    input: TradingAgentChatDto,
    practice_agent_service: PracticeService = Depends(lambda: PracticeService()),
):
    return practice_agent_service.chat_practice_agent(input.message)


@router.post("/trade/chat", tags=["trade"])
async def chat_trade_agent(
    input: TradingAgentChatDto,
    trade_agent_service: TradingAgentService = Depends(lambda: TradingAgentService()),
):
    return trade_agent_service.trade_trading_agent(input.message)
