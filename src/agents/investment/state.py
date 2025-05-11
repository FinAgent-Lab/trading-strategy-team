from typing import TypedDict, Annotated
from src.agents.common.states.common import CommonState


class InvestmentState(TypedDict):
    # DB 관련 공통 속성
    common: Annotated[CommonState, "common"]

    account_number: Annotated[str, "account number"]

    last_state: Annotated[str, "error | content | tool_call"]
