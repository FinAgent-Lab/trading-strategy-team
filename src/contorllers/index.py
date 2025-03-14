from fastapi import APIRouter
from src.contorllers.agent import agent_router

index_router = router = APIRouter(prefix="/api")

index_router.include_router(agent_router)
