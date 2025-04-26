from langchain_openai import ChatOpenAI
from typing_extensions import Self
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from src.config import Global
from src.agents.ideaAgent.state import IdeaState
from src.agents.ideaAgent.node import IdeaNode

class IdeaGraph:
    _builder: StateGraph
    graph: CompiledStateGraph

    def __init__(self):
        self._builder = StateGraph(IdeaState)
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=Global.env.OPENAI_API_KEY)
        self.build()

    def build(self) -> Self:
        # 가설 생성 노드 추가
        self._builder.add_node("generate_hypothesis", IdeaNode(self.llm))

        # 시작 엣지 설정
        self._builder.add_edge(START, "generate_hypothesis")

        # 조건부 엣지 추가
        def should_continue(state: IdeaState) -> str:
            """가설 생성이 완료되면 종료"""
            if state["hypothesis"]:
                return END
            return "generate_hypothesis"

        self._builder.add_conditional_edges(
            "generate_hypothesis",
            should_continue,
            {"generate_hypothesis": "generate_hypothesis", END: END}
        )

        self.graph = self._builder.compile()
        return self

    def get_nodes(self) -> dict[str, any]:
        return self._builder.nodes()

    def get_edges(self) -> list[tuple[str, str]]:
        return self._builder.edges()

    def invoke(self, input: dict[str, any]):
        print(f"Graph input: {input}")
        response = self.graph.invoke(input)
        res = response["messages"][-1].content
        print(f"Graph response: {res}")
        return res 