from typing import TypedDict, Annotated
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from src.agents.common.states.common import CommonState


class ChartAnalysisState(TypedDict):
    # DB 관련 공통 속성
    common: Annotated[CommonState, "common"]

    symbol: Annotated[str, "symbol"]
    exchange: Annotated[str, "exchange"]
    df: Annotated[any, "dataframe"]
    column_description: Annotated[str | None, "column description"]
    chart_analysis: Annotated[str | None, "chart analysis"]
    future_prediction: Annotated[str | None, "future prediction"]
