from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.services.chartAnalysis import ChartAnalysisService

chart_analysis_router = router = APIRouter(prefix="/chart-analysis")


class ChartAnalysisRequest(BaseModel):
    symbol: str
    exchange: str = "NAS"


@router.post("/analyze")
async def analyze_stock_chart(
    input: ChartAnalysisRequest,
    chart_analysis_service: ChartAnalysisService = Depends(lambda: ChartAnalysisService()),
):
    """주식 차트 분석을 수행합니다."""
    return chart_analysis_service.analyze_stock(input.symbol, input.exchange) 