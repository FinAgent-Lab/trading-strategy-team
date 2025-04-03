from fastapi import APIRouter
from src.controllers.agent import agent_router
from src.controllers.kis import kis_router
from src.controllers.chartAnalysis import chart_analysis_router

index_router = router = APIRouter(prefix="/api")

index_router.include_router(agent_router)
index_router.include_router(kis_router)
index_router.include_router(chart_analysis_router)
