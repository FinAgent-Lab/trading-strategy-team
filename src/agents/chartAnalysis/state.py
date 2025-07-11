from typing import TypedDict, Annotated


class ChartAnalysisState(TypedDict):
    symbol: Annotated[str, "symbol"]
    exchange: Annotated[str, "exchange"]
    df: Annotated[any, "dataframe"]
    column_description: Annotated[str | None, "column description"]
    chart_analysis: Annotated[str | None, "chart analysis"]
    future_prediction: Annotated[str | None, "future prediction"]
