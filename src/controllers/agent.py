from fastapi import APIRouter, Depends
from src.services.practice import PracticeService
from src.dtos.tradingAgent.chatDto import TradingAgentChatDto
from src.services.tradingAgent import TradingAgentService
from src.services.chartAnalysis import ChartAnalysisService
from src.dtos.chartAnalysis.analysisDto import ChartAnalysisRequest
from src.services.kis import KisService
from langchain_core.tools import tool, Tool

agent_router = router = APIRouter(prefix="/agent")

kis_service = KisService()

@tool
def get_stock_data(input: dict):
    """해외 주식 일별 시세를 조회합니다."""
    return kis_service.get_overseas_stock_daily_price(input)

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


@router.post("/chart-analysis", tags=["chart-analysis"])
async def analyze_stock_chart(
    input: ChartAnalysisRequest,
    chart_analysis_service: ChartAnalysisService = Depends(lambda: ChartAnalysisService())
):
    """주식 차트를 분석하고 결과를 반환합니다."""
    return chart_analysis_service.analyze_stock(
        symbol=input.symbol,
        exchange=input.exchange
    )
