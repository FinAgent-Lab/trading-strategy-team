from src.agents.chartAnalysis.graph import ChartAnalysisGraph
from src.agents.idea.ideaAgent import IdeaAgent
from src.agents.investment.graph import InvestmentGraph
from src.agents.factor.graph import factor_agent_graph
from src.agents.supervisor.graph import SupervisorGraph
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage
from src.agents.supervisor.state import SupervisorState
from src.services.user import UserService


class TradeAgentService:
    _instance = None
    investment_agent: InvestmentGraph
    chart_analysis_agent: ChartAnalysisGraph
    idea_agent: IdeaAgent
    factor_agent: CompiledStateGraph
    trade_agent: SupervisorGraph
    user_service: UserService

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # 초기화 코드 (한 번만 호출됨)
        if not hasattr(
            self, "_initialized"
        ):  # 이미 초기화된 경우는 다시 초기화하지 않음
            self._initialized = True
            self._data = {}
            # Main Trade Agent
            self.trade_agent = SupervisorGraph()
            self.user_service = UserService()

            # Extra Agents
            self.investment_agent = InvestmentGraph()
            self.chart_analysis_agent = ChartAnalysisGraph()
            self.idea_agent = IdeaAgent()
            # self.factor_agent = factor_agent_graph()

    async def chat_trade_agent(self, room_id: str, user_id: str, input: str):
        user_info = await self.user_service.get_user_info(user_id)

        state: SupervisorState = {
            "common": {
                "room": {
                    "id": room_id,
                },
                "user": {
                    "id": user_id,
                    "account_number": user_info["account_number"],
                    "app_key": user_info["app_key"],
                    "app_secret": user_info["secret_key"],
                    "access_token": user_info["access_token"],
                },
                "messages": [HumanMessage(input)],
            },
        }

        return await self.trade_agent.invoke(state)

    async def chat_investment_agent(self, room_id: str, user_id: str, input: str):
        user_info = await self.user_service.get_user_info(user_id)

        state: SupervisorState = {
            "common": {
                "room": {"id": room_id},
                "user": {
                    "id": user_id,
                    "account_number": user_info["account_number"],
                    "app_key": user_info["app_key"],
                    "app_secret": user_info["secret_key"],
                    "access_token": user_info["access_token"],
                },
                "messages": [HumanMessage(input)],
            },
        }
        return await self.investment_agent.invoke(state)

    async def chat_chart_analysis_agent(self, room_id: str, user_id: str, input: str):
        return await self.chart_analysis_agent.invoke(room_id, user_id, input)

    async def chat_idea_agent(self, room_id: str, user_id: str, input: str):
        return await self.idea_agent.invoke(room_id, user_id, input)

    # async def chat_factor_agent(self, room_id: str, user_id: str, input: str):
    #     return await self.factor_agent.ainvoke(room_id, user_id, input)
