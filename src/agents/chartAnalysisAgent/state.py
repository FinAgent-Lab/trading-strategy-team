from typing import TypedDict, Annotated, Optional
from langgraph.graph import add_messages
import pandas as pd


class ChartAnalysisState(TypedDict):
    symbol: str
    exchange: str
    df: Optional[pd.DataFrame]
    column_description: Optional[str]
    chart_analysis: Optional[str]
    future_prediction: Optional[str]
    messages: Annotated[list, add_messages]