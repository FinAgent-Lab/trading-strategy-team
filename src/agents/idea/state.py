from typing import TypedDict, Annotated
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from src.agents.common.states.common import CommonState


class HypothesisDict(TypedDict):
    hypothesis: str
    confidence: float


class IdeaState(TypedDict, total=False):
    # DB 관련 공통 속성
    common: Annotated[CommonState, "common"]

    hypothesis: Annotated[dict, "종목별 생성된 가설 정보"]
    status: Annotated[str, "현재 상태(success, failed, pending)"]
    iteration_count: Annotated[int, "iteration count"]
