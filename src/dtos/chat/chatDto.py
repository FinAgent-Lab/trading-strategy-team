from pydantic import BaseModel
from src.utils.types.ChatType import ChatRole, ChatAgent


class CreateChatDto(BaseModel):
    content: str
    role: ChatRole
    agent: ChatAgent
