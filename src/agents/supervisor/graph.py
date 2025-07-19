from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from src.agents.supervisor.node import SupervisorNode
from src.agents.supervisor.state import SupervisorState
from src.dtos.chat.chatDto import CreateChatDto
from src.services.chat import ChatService
from src.utils.graphBuilder import GraphBuilder
from src.config import Global
from src.agents.investment.graph import InvestmentGraph
from src.agents.chartAnalysis.graph import ChartAnalysisGraph
from src.agents.idea.graph import IdeaGraph
from src.agents.factor.graph import factor_agent_graph
from src.utils.types.ChatType import ChatAgent, ChatRole
from src.utils.types.PromptType import PromptType
import traceback
from src.utils.logger import logger


class SupervisorGraph(GraphBuilder):
    _builder: StateGraph
    graph: CompiledStateGraph
    chat_service: ChatService

    def __init__(self):
        self.chat_service = ChatService()

        self._builder = StateGraph(SupervisorState)
        self.llm = ChatOpenAI(model="gpt-4.1", api_key=Global.env.OPENAI_API_KEY)
        self.build()

    def build(self):
        self._builder.add_node("supervisor", SupervisorNode(self.llm))
        self._builder.add_node("chart_analysis", ChartAnalysisGraph(self.llm).invoke)
        self._builder.add_node("idea", IdeaGraph(self.llm).invoke)
        self._builder.add_node("factor", factor_agent_graph().invoke)
        self._builder.add_node("investment", InvestmentGraph().invoke)

        # 노드 연결
        # self._builder.add_edge(START, "chart_analysis")
        # self._builder.add_edge("chart_analysis", "idea")
        # self._builder.add_edge("idea", "factor")
        # self._builder.add_edge("factor", "investment")
        # self._builder.add_edge("investment", END)

        def get_next_node(state: SupervisorState) -> str:
            response = state["common"]["messages"][-1].content
            if response == "chart-analysis":
                return "chart_analysis"
            elif response == "idea":
                return "idea"
            elif response == "factor":
                return "factor"
            elif response == "investment":
                return "investment"
            else:
                return END

        self._builder.add_edge(START, "supervisor")
        self._builder.add_conditional_edges(
            "supervisor",
            get_next_node,
            path_map={
                "chart_analysis": "chart_analysis",
                "idea": "idea",
                "factor": "factor",
                "investment": "investment",
                END: END,
            },
        )
        self._builder.add_edge("chart_analysis", "supervisor")
        self._builder.add_edge("idea", "supervisor")
        self._builder.add_edge("factor", "supervisor")
        self._builder.add_edge("investment", "supervisor")

        self.graph = self._builder.compile()

        return self.graph

    def get_nodes(self) -> dict[str, any]:
        return self._builder.nodes()

    def get_edges(self) -> list[tuple[str, str]]:
        return self._builder.edges()

    async def invoke(self, state: SupervisorState):
        print(
            f"--------------------------------Supervisor input: {state['common']['messages'][-1]}--------------------------------"
        )
        try:
            response: SupervisorState = await self.graph.ainvoke(state)

            response["common"]["messages"][-1]

        except Exception as e:
            logger.error("\n\n\n🚨🚨🚨🚨🚨🚨🚨🚨 - Error Occurs - 🚨🚨🚨🚨🚨🚨🚨🚨\n")
            logger.error(traceback.format_exc())
            logger.error("\n🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨\n\n\n")
            state["common"]["messages"].append(
                PromptType(
                    role=ChatRole.ASSISTANT,
                    content=e.__str__(),
                )
            )
            res: SupervisorState = await self.graph.ainvoke(state)
            return res
        print(
            f"--------------------------------Supervisor response: {response['common']['messages'][-1]}--------------------------------\n"
        )

        return state
