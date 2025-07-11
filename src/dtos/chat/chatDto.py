from datetime import datetime
from pydantic import BaseModel
from src.utils.types.ChatType import ChatRole, ChatAgent


class CreateChatDto(BaseModel):
    content: str
    role: ChatRole
    agent: ChatAgent


class ChatListDto(BaseModel):
    id: str
    content: str
    role: ChatRole
    agent: ChatAgent
    created_at: datetime


class GetChatListDto(BaseModel):
    chats: list[ChatListDto]
