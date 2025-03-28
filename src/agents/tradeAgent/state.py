from typing import TypedDict, Annotated
from langgraph.graph import add_messages


class TradeState(TypedDict):
    messages: Annotated[list, add_messages]
    processed: Annotated[list, add_messages]
