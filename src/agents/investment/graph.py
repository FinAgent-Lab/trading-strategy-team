from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from src.agents.supervisor.state import SupervisorState
from src.config import Global
from src.agents.investment.state import InvestmentState
from src.agents.investment.node import InvestmentNode
from src.utils.graphBuilder import GraphBuilder
from src.services.chat import ChatService


class InvestmentGraph(GraphBuilder):
    _builder: StateGraph
    graph: CompiledStateGraph
    chat_service: ChatService

    def __init__(self, llm: ChatOpenAI | None = None):
        self.chat_service = ChatService()
        self.llm = (
            llm
            if llm
            else ChatOpenAI(model="gpt-4.1", api_key=Global.env.OPENAI_API_KEY)
        )
        # TemplateState 자리에 사용할 State를 넣어주세요.
        self._builder = StateGraph(InvestmentState)
        self.build()

    def build(self):

        ##############추가할 노드를 여기에 작성해주세요.###############
        self._builder.add_node("trade", InvestmentNode(self.llm))

        #######################################################

        # 시작 엣지. 시작할 노드를 적어주세요.
        self._builder.add_edge(START, "trade")
        self._builder.add_edge("trade", END)
        # self._builder.add_edge("trade", "trade")

        # 조건부 엣지 추가
        # def should_continue(state: TradeState) -> str:
        #     """LLM 응답에 tool call이 있으면 'trade'로, 없으면 'end'로 이동"""
        #     if state["processed"][-1].content == "content":
        #         return END
        #     return "trade"

        # self._builder.add_conditional_edges(
        #     "trade", should_continue, {"trade": "trade", END: END}
        # )

        ###############추가할 엣지를 여기에 작성해주세요.##############

        #######################################################

        # 종료 엣지. 마지막 노드를 적어주세요.
        # self._builder.add_edge("trade", END)

        self.graph = self._builder.compile()
        return self.graph

    def get_nodes(self) -> dict[str, any]:
        return self._builder.nodes()

    def get_edges(self) -> list[tuple[str, str]]:
        return self._builder.edges()

    async def invoke(self, state: SupervisorState):

        print(
            f"--------------------------------Investment input: {state['common']['messages'][-1]}--------------------------------"
        )
        response: InvestmentState = await self.graph.ainvoke(state)
        res = response["common"]["messages"][-1]
        print(
            f"--------------------------------Investment response: {response['common']['messages'][-1]}--------------------------------\n"
        )

        return res
