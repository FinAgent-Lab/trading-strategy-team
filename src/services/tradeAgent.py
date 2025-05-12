from src.agents.chartAnalysis.graph import ChartAnalysisGraph
from src.agents.idea.ideaAgent import IdeaAgent
from src.agents.investment.graph import InvestmentGraph
from src.agents.factor.graph import factor_agent_graph
from src.agents.supervisor.graph import SupervisorGraph
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage
from src.agents.supervisor.state import SupervisorState
from src.dtos.chat.chatDto import CreateChatDto
from src.services.chat import ChatService
from src.services.kis import KisService
from src.services.user import UserService
from src.utils.types.ChatType import ChatAgent, ChatRole
from src.utils.types.PromptType import PromptType


class TradeAgentService:
    _instance = None
    investment_agent: InvestmentGraph
    chart_analysis_agent: ChartAnalysisGraph
    idea_agent: IdeaAgent
    factor_agent: CompiledStateGraph
    trade_agent: SupervisorGraph
    user_service: UserService
    chat_service: ChatService
    kis_service: KisService

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

            self.user_service = UserService()
            self.chat_service = ChatService()
            self.kis_service = KisService()

            # Main Trade Agent
            self.trade_agent = SupervisorGraph()

            # Extra Agents
            self.investment_agent = InvestmentGraph()
            self.chart_analysis_agent = ChartAnalysisGraph()
            self.idea_agent = IdeaAgent()
            # self.factor_agent = factor_agent_graph()

    async def chat_trade_agent(self, room_id: str, user_id: str, input: str):

        access_token = await self.kis_service.get_access_token(user_id)

        user_info = await self.user_service.get_user_info(user_id)

        history = await self.chat_service.get_chat_list(room_id)

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
                    "access_token": access_token,
                },
                "messages": [PromptType(role=ChatRole.USER, content=input)],
                "history": history.chats,
            },
        }

        await self.chat_service.create_chat(
            room_id,
            user_id,
            CreateChatDto(content=input, role=ChatRole.USER, agent=ChatAgent.HUMAN),
        )

        res = await self.trade_agent.invoke(state)

        await self.chat_service.create_chat(
            room_id,
            user_id,
            CreateChatDto(
                content=res["common"]["messages"][-1].content,
                role=ChatRole.ASSISTANT,
                agent=ChatAgent.TRADE,
            ),
        )

        return res["common"]["messages"][-1]

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
                "messages": [PromptType(role=ChatRole.USER, content=input)],
            },
        }
        return await self.investment_agent.invoke(state)

    async def chat_chart_analysis_agent(self, room_id: str, user_id: str, input: str):
        return await self.chart_analysis_agent.invoke(room_id, user_id, input)

    async def chat_idea_agent(self, room_id: str, user_id: str, input: str):
        return await self.idea_agent.invoke(room_id, user_id, input)

    # async def chat_factor_agent(self, room_id: str, user_id: str, input: str):
    #     return await self.factor_agent.ainvoke(room_id, user_id, input)
