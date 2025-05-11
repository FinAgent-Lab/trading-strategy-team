from typing import Annotated, TypedDict
from langgraph.graph import add_messages
from src.agents.common.states.roomInfo import RoomInfo
from src.agents.common.states.userInfo import UserInfo
from src.utils.types.PromptType import PromptType


class CommonState(TypedDict):
    user: Annotated[UserInfo, "user_info"]
    room: Annotated[RoomInfo, "room_info"]
    # Short term memory
    messages: Annotated[list[PromptType], "history"]
