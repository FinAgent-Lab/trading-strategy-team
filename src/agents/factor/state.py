from typing import Annotated, TypedDict
from src.agents.common.states.common import CommonState


class FactorAgentState(TypedDict):
    # DB 관련 공통 속성
    common: Annotated[CommonState, "common"]

    hypothesis: Annotated[dict, "종목별 생성된 가설 정보"]
    ast: dict
    alpha: dict
    final_alpha: dict
    rebalance_value: dict
    rebalance_shares: dict
