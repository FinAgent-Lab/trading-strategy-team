from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class HypothesisDict(TypedDict):
    hypothesis: str
    confidence: float

class IdeaState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    hypotheses: Annotated[dict, "종목별 생성된 가설 정보"]
    status: Annotated[str, "현재 상태(success, failed, pending)"]
    iteration_count: int
