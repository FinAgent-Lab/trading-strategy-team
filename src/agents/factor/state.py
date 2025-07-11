from typing import Annotated, TypedDict


class FactorAgentState(TypedDict):
    hypothesis: Annotated[dict, "종목별 생성된 가설 정보"]
    ast: dict
    alpha: dict
    final_alpha: dict
    rebalance_value: dict
    rebalance_shares: dict
    closed_prices: dict
