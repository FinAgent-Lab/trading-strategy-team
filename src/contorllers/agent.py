from fastapi import APIRouter
from src.services.agent import get_agent

agent_router = router = APIRouter(prefix="/api/agent")


@router.get("/")
def agent(data: str, model: str):
    return get_agent()
