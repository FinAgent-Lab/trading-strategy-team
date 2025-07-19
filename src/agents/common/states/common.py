from typing import Annotated, TypedDict
from langgraph.graph import add_messages
from src.agents.common.states.roomInfo import RoomInfo
from src.agents.common.states.userInfo import UserInfo
from src.utils.types.PromptType import PromptType
from src.dtos.chat.chatDto import ChatListDto


class CommonState(TypedDict):
    user: Annotated[UserInfo, "user_info"]
    room: Annotated[RoomInfo, "room_info"]
    # Short term memory including user's message, tool call and agent's response
    messages: Annotated[list[PromptType], "short term memory"]

    # history of entire conversation
    history: Annotated[list[ChatListDto], "history"]
