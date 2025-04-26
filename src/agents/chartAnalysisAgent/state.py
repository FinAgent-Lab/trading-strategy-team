from typing import TypedDict, Annotated
from langgraph.graph import add_messages


class ChartAnalysisState(TypedDict):
    messages: Annotated[list, add_messages]
    processed: Annotated[list, add_messages]
    symbol: str
    exchange: str
    access_token: str
    df: any
    column_description: str | None
    chart_analysis: str | None
    future_prediction: str | None