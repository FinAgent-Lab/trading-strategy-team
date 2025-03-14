from fastapi import APIRouter, Depends
from src.dtos.tradingAgent.chatDto import TradingAgentChatDto
from src.services.tradingAgent import TradingAgentService

agent_router = router = APIRouter(prefix="/agent")


@router.post("/trading/chat")
async def chat_trading_agent(
    input: TradingAgentChatDto,
    trading_agent_service: TradingAgentService = Depends(lambda: TradingAgentService()),
):
    return trading_agent_service.chat_trading_agent(input.message)
