from typing import TypedDict, Annotated
from langgraph.graph import add_messages


class TradeState(TypedDict):
    room_id: str
    user_id: str
    account_number: str
    # processed: Annotated[list[str], add_messages]
    messages: Annotated[list[str], add_messages]
    last_state: Annotated[str, "error | content | tool_call"]
