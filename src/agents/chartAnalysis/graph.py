import json
from langchain_openai import ChatOpenAI
from typing_extensions import Self
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from src.config import Global
from src.agents.chartAnalysis.state import ChartAnalysisState
from src.agents.chartAnalysis.node import ChartAnalysisNode
from src.utils.graphBuilder import GraphBuilder


class ChartAnalysisGraph(GraphBuilder):
    _builder: StateGraph
    graph: CompiledStateGraph

    def __init__(self, llm: ChatOpenAI | None = None):
        self._builder = StateGraph(ChartAnalysisState)
        self.llm = (
            llm
            if llm
            else ChatOpenAI(
                model="gpt-4o-mini",
                api_key=Global.env.OPENAI_API_KEY,
            )
        )
        self.build()

    def build(self):
        # 노드 추가
        self._builder.add_node("analyze", ChartAnalysisNode(self.llm))

        # 시작 엣지
        self._builder.add_edge(START, "analyze")

        # 종료 엣지 - 분석이 완료되면 바로 종료
        self._builder.add_edge("analyze", END)

        self.graph = self._builder.compile()
        return self.graph

    def get_nodes(self) -> dict[str, any]:
        return self._builder.nodes()

    def get_edges(self) -> list[tuple[str, str]]:
        return self._builder.edges()

    async def invoke(self, state: ChartAnalysisState):

        print(f"Chart Analysis input: {state['common']['messages'][-1]}")
        response: ChartAnalysisState = await self.graph.ainvoke(state)
        print(f"Chart Analysis After state: {state}")

        return state
