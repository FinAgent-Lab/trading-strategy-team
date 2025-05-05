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
        self._builder.add_node("generate_hypothesis", IdeaNode(self.llm))
        self._builder.add_edge(START, "generate_hypothesis")

        def should_continue(state: IdeaState) -> str:
            iteration_count = state.get("iteration_count")
            if iteration_count is None:
                iteration_count = 0
            status = state.get("status") or "pending"

            if iteration_count >= 3:
                return END

            if status in ["success", "failed"]:
                return END

            state["iteration_count"] = iteration_count + 1
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

    async def invoke(self, input: dict[str, any]):
        print(f"Graph input: {input}")
        response = await self.graph.ainvoke(input)
        print(f"Graph response: {response}")
        return response.get("hypotheses", {})