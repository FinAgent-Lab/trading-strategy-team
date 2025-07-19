from typing import Annotated
from fastapi import APIRouter, Depends, Path
from src.guards.jwtGuard import jwt_guard
from src.dtos.tradingAgent.chatDto import TradingAgentChatDto
from src.services.tradeAgent import TradeAgentService
from src.services.chartAnalysis import ChartAnalysisService
from src.dtos.chartAnalysis.analysisDto import ChartAnalysisRequest
from src.services.kis import KisService
from langchain_core.tools import tool

agent_router = router = APIRouter()

kis_service = KisService()


@router.post("/trade/room/{room_id}/chat")
async def chat_trade_agent(
    room_id: Annotated[str, Path()],
    user_id: Annotated[str, Depends(jwt_guard)],
    input: TradingAgentChatDto,
    trade_agent_service: TradeAgentService = Depends(lambda: TradeAgentService()),
):

    return await trade_agent_service.chat_trade_agent(room_id, user_id, input.message)


@router.post("/chart-analysis", tags=["chart-analysis"])
async def analyze_stock_chart(
    input: ChartAnalysisRequest,
    chart_analysis_service: ChartAnalysisService = Depends(
        lambda: ChartAnalysisService()
    ),
):
    """주식 차트를 분석하고 결과를 반환합니다."""
    return chart_analysis_service.analyze_stock(
        symbol=input.symbol, exchange=input.exchange
    )


@router.post("/investment/room/{room_id}/chat", tags=["investment"])
async def chat_investment_agent(
    room_id: Annotated[str, Path()],
    user_id: Annotated[str, Depends(jwt_guard)],
    input: TradingAgentChatDto,
    trade_agent_service: TradeAgentService = Depends(lambda: TradeAgentService()),
):
    return await trade_agent_service.chat_investment_agent(
        room_id, user_id, input.message
    )


@router.post("/idea/room/{room_id}/chat", tags=["idea"])
async def chat_idea_agent(
    room_id: Annotated[str, Path()],
    user_id: Annotated[str, Depends(jwt_guard)],
    input: TradingAgentChatDto,
    trade_agent_service: TradeAgentService = Depends(lambda: TradeAgentService()),
):
    return await trade_agent_service.chat_idea_agent(room_id, user_id, input.message)


@router.post("/factor/room/{room_id}/chat", tags=["factor"])
async def chat_factor_agent(
    room_id: Annotated[str, Path()],
    user_id: Annotated[str, Depends(jwt_guard)],
    input: TradingAgentChatDto,
    trade_agent_service: TradeAgentService = Depends(lambda: TradeAgentService()),
):
    return await trade_agent_service.chat_factor_agent(room_id, user_id, input.message)
