from langchain_openai import ChatOpenAI
from typing_extensions import Self
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from src.config import Global
from src.agents.chartAnalysisAgent.state import ChartAnalysisState
from src.agents.chartAnalysisAgent.node import ChartAnalysisNode
from src.utils.graphBuilder import GraphBuilder


class ChartAnalysisGraph(GraphBuilder):
    _builder: StateGraph
    graph: CompiledStateGraph

    def __init__(self):
        self._builder = StateGraph(ChartAnalysisState)
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=Global.env.OPENAI_API_KEY)
        self.build()

    def build(self) -> Self:
        # 노드 추가
        self._builder.add_node("analyze", ChartAnalysisNode(self.llm))

        # 시작 엣지
        self._builder.add_edge(START, "analyze")
        
        # 종료 엣지 - 분석이 완료되면 바로 종료
        self._builder.add_edge("analyze", END)

        self.graph = self._builder.compile()
        return self

    def get_nodes(self) -> dict[str, any]:
        return self._builder.nodes()

    def get_edges(self) -> list[tuple[str, str]]:
        return self._builder.edges()

    def invoke(self, input: dict[str, any]):
        print(f"Graph input: {input}")
        response = self.graph.invoke(input)
        res = response["messages"][-1]
        print(f"Graph response: {res}")
        return res