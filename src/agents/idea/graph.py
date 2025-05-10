import json
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from src.config import Global
from src.agents.idea.state import IdeaState
from src.agents.idea.node import IdeaNode
from src.utils.graphBuilder import GraphBuilder


class IdeaGraph(GraphBuilder):
    _builder: StateGraph
    graph: CompiledStateGraph

    def __init__(self, llm: ChatOpenAI | None = None):
        self._builder = StateGraph(IdeaState)
        self.llm = (
            llm
            if llm
            else ChatOpenAI(model="gpt-4o-mini", api_key=Global.env.OPENAI_API_KEY)
        )
        self.build()

    def build(self):
        self._builder.add_node("generate_hypothesis", IdeaNode(self.llm))
        self._builder.add_edge(START, "generate_hypothesis")

        # def should_continue(state: IdeaState) -> str:
        #     iteration_count = state.get("iteration_count")
        #     if iteration_count is None:
        #         iteration_count = 0
        #     status = state.get("status") or "pending"

        #     if iteration_count >= 3:
        #         return END

        #     if status in ["success", "failed"]:
        #         return END

        #     state["iteration_count"] = iteration_count + 1
        #     return "generate_hypothesis"

        # self._builder.add_conditional_edges(
        #     "generate_hypothesis",
        #     should_continue,
        #     {"generate_hypothesis": "generate_hypothesis", END: END},
        # )

        self.graph = self._builder.compile()
        return self.graph

    def get_nodes(self) -> dict[str, any]:
        return self._builder.nodes()

    def get_edges(self) -> list[tuple[str, str]]:
        return self._builder.edges()

    async def invoke(self, state: IdeaState):
        room_id = state["common"]["room"]["id"]
        user_id = state["common"]["user"]["id"]

        print(f"Idea input: {state['common']['messages'][-1]}")
        response: IdeaState = await self.graph.ainvoke(state)
        state["hypothesis"] = response["hypothesis"]
        print(f"Idea response: {state}")
        return state
