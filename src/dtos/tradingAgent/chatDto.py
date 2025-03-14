from pydantic import BaseModel


class TradingAgentChatDto(BaseModel):
    message: str
