from typing import TypedDict, Annotated


class InvestmentState(TypedDict):
    account_number: Annotated[str, "account number"]
    last_state: Annotated[str, "error | content | tool_call"]
