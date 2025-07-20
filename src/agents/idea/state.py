from typing import TypedDict, Annotated


# class HypothesisDict(TypedDict):
#     hypothesis: str
#     confidence: float


class IdeaState(TypedDict, total=False):
    hypothesis: Annotated[dict, "종목별 생성된 가설 정보"]
    status: Annotated[str, "현재 상태(success, failed, pending)"]
    iteration_count: Annotated[int, "iteration count"]
