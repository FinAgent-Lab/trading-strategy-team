from typing import TypedDict, Annotated
from langgraph.graph import add_messages


class HypothesisDict(TypedDict):
    hypothesis: str
    confidence: float

class IdeaState(TypedDict):
    messages: Annotated[list, add_messages]
    hypothesis: Annotated[HypothesisDict, "현재 생성된 가설 정보"]
