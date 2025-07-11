from typing import Annotated, TypedDict
from src.agents.chartAnalysis.state import ChartAnalysisState
from src.agents.idea.state import IdeaState
from src.agents.factor.state import FactorAgentState
from src.agents.investment.state import InvestmentState
from src.agents.common.state import CommonState


class State(TypedDict):
    common: Annotated[CommonState, "common"]

    # State of each agent
    chart_analysis: Annotated[ChartAnalysisState, "chart analysis"]
    idea: Annotated[IdeaState, "idea"]
    factor: Annotated[FactorAgentState, "factor"]
    investment: Annotated[InvestmentState, "investment"]
