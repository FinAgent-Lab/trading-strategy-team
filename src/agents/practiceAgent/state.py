from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


# State의 add_messages 함수는 이미 상태에 있는 메시지에 llm의 응답 메시지를 추가한다.
class State(TypedDict):
    messages: Annotated[list, add_messages]
