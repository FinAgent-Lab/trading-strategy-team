from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from src.agents.supervisor.node import SupervisorNode
from src.agents.supervisor.state import State
from src.utils.graphBuilder import GraphBuilder
from src.config import Global
from src.agents.investment.graph import InvestmentGraph
from src.agents.chartAnalysis.graph import ChartAnalysisGraph
from src.agents.idea.graph import IdeaGraph
from src.agents.factor.graph import factor_agent_graph
from src.utils.types.ChatType import ChatRole
from src.utils.types.PromptType import PromptType
import traceback
from src.utils.logger import logger


class SupervisorGraph(GraphBuilder):
    _builder: StateGraph
    graph: CompiledStateGraph

    def __init__(self):

        self._builder = StateGraph(State)
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            model="openai/gpt-4.1",
            # model="anthropic/claude-3.7-sonnet",
            api_key=Global.env.OPENAI_API_KEY,
        )
        self.build()

    def build(self):
        self._builder.add_node("supervisor_node", SupervisorNode(self.llm))
        self._builder.add_node(
            "chart_analysis_graph", ChartAnalysisGraph(self.llm).invoke
        )
        self._builder.add_node("idea_graph", IdeaGraph(self.llm).invoke)
        self._builder.add_node("factor_graph", factor_agent_graph(self.llm).invoke)
        self._builder.add_node("investment_graph", InvestmentGraph(self.llm).invoke)

        def get_next_node(state: State) -> str:
            response = state["common"]["messages"][-1].content
            if response == "chart-analysis":
                return "chart_analysis_graph"
            elif response == "idea":
                return "idea_graph"
            elif response == "factor":
                return "factor_graph"
            elif response == "investment":
                return "investment_graph"
            else:
                return END

        self._builder.add_edge(START, "supervisor_node")
        self._builder.add_conditional_edges(
            "supervisor_node",
            get_next_node,
            path_map={
                "chart_analysis_graph": "chart_analysis_graph",
                "idea_graph": "idea_graph",
                "factor_graph": "factor_graph",
                "investment_graph": "investment_graph",
                END: END,
            },
        )

        # self._builder.add_edge("chart_analysis_graph", "supervisor_node")
        # self._builder.add_edge("idea_graph", "supervisor_node")
        # self._builder.add_edge("factor_graph", "supervisor_node")
        # self._builder.add_edge("investment_graph", "supervisor_node")

        self._builder.add_edge("chart_analysis_graph", "idea_graph")
        self._builder.add_edge("idea_graph", "factor_graph")
        self._builder.add_edge("factor_graph", "investment_graph")

        self._builder.add_edge("investment_graph", END)

        self.graph = self._builder.compile()

        return self.graph

    def get_nodes(self) -> dict[str, any]:
        return self._builder.nodes()

    def get_edges(self) -> list[tuple[str, str]]:
        return self._builder.edges()

    async def invoke(self, state: State):
        print(f"User Input: {state['common']['messages'][0].content}")
        print()

        try:
            response: State = await self.graph.ainvoke(state)

        except Exception as e:
            logger.error("\n\n\n🚨🚨🚨🚨🚨🚨🚨🚨 - Error Occurs - 🚨🚨🚨🚨🚨🚨🚨🚨\n")
            logger.error(traceback.format_exc())
            logger.error("\n🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨\n\n\n")
            state["common"]["messages"].append(
                PromptType(
                    role=ChatRole.USER,
                    content="\n".join(
                        [
                            f"Error Message: {e.__str__()}",
                            "Please Response with My First Message's Language.",
                        ]
                    ),
                )
            )
            res: State = await self.graph.ainvoke(state)
            return res

        return response
