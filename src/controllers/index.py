from fastapi import APIRouter

from src.controllers.agent import agent_router
from src.controllers.kis import kis_router
from src.controllers.user import user_router
from src.controllers.chat import chat_router

index_router = router = APIRouter(prefix="/api")

index_router.include_router(agent_router)
index_router.include_router(kis_router)
index_router.include_router(user_router)
index_router.include_router(chat_router)
