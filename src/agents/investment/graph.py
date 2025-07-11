from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from src.agents.supervisor.state import State
from src.config import Global
from src.agents.investment.node import InvestmentNode
from src.utils.graphBuilder import GraphBuilder


class InvestmentGraph(GraphBuilder):
    _builder: StateGraph
    graph: CompiledStateGraph

    def __init__(self, llm: ChatOpenAI | None = None):
        self.llm = (
            llm
            if llm
            else ChatOpenAI(model="gpt-4.1", api_key=Global.env.OPENAI_API_KEY)
        )
        # TemplateState 자리에 사용할 State를 넣어주세요.
        self._builder = StateGraph(State)
        self.build()

    def build(self):

        ##############추가할 노드를 여기에 작성해주세요.###############
        self._builder.add_node("trade", InvestmentNode(self.llm))

        #######################################################

        # 시작 엣지. 시작할 노드를 적어주세요.
        self._builder.add_edge(START, "trade")
        self._builder.add_edge("trade", END)

        self.graph = self._builder.compile()
        return self.graph

    def get_nodes(self) -> dict[str, any]:
        return self._builder.nodes()

    def get_edges(self) -> list[tuple[str, str]]:
        return self._builder.edges()

    async def invoke(self, state: State):
        response: State = await self.graph.ainvoke(state)
        return response
