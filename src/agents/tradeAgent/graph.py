from langchain_openai import ChatOpenAI
from typing_extensions import Self
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from src.config import Global
from src.agents.tradeAgent.state import TradeState
from src.agents.tradeAgent.tradeNode import TradeNode
from src.utils.graphBuilder import GraphBuilder


class TradeGraph(GraphBuilder):
    _builder: StateGraph
    graph: CompiledStateGraph

    def __init__(self):
        # TemplateState 자리에 사용할 State를 넣어주세요.
        self._builder = StateGraph(TradeState)
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=Global.env.OPENAI_API_KEY)

        self.build()

    def build(self) -> Self:

        ##############추가할 노드를 여기에 작성해주세요.###############
        self._builder.add_node("trade", TradeNode(self.llm))

        #######################################################

        # 시작 엣지. 시작할 노드를 적어주세요.
        self._builder.add_edge(START, "trade")
        # self._builder.add_edge("trade", "trade")

        # 조건부 엣지 추가
        def should_continue(state: TradeState) -> str:
            """LLM 응답에 tool call이 있으면 'trade'로, 없으면 'end'로 이동"""
            if state["processed"][-1].content == "content":
                return END
            return "trade"

        self._builder.add_conditional_edges(
            "trade", should_continue, {"trade": "trade", END: END}
        )

        ###############추가할 엣지를 여기에 작성해주세요.##############

        #######################################################

        # 종료 엣지. 마지막 노드를 적어주세요.
        # self._builder.add_edge("trade", END)

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
