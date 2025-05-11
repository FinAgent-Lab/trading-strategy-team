from fastapi import APIRouter

from src.controllers.agent import agent_router

# from src.controllers.kis import kis_router
from src.controllers.user import user_router
from src.controllers.chat import chat_router

index_router = router = APIRouter(prefix="/api")

index_router.include_router(agent_router, prefix="/agent", tags=["Agent"])
# index_router.include_router(kis_router, prefix="/kis", tags=["KIS"])
index_router.include_router(user_router, prefix="/user", tags=["User"])
index_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
