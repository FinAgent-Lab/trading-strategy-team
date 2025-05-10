from typing import Annotated, TypedDict
from src.agents.common.states.common import CommonState


class SupervisorState(TypedDict):
    common: Annotated[CommonState, "common"]

    # Supervisor의 각 노드(여기서는 Graph)에서 사용되는 상태
    hypothesis: Annotated[dict, "종목별 생성된 가설 정보"]

    final_alpha: Annotated[dict, "종목별 최종 알파 값"]
