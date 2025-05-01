from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from langgraph.graph import START, END
from src.agents.factorAgent.node import FactorAgent

class FactorAgentState(TypedDict):
    hypothesis: dict
    ast: dict
    alpha: dict
    final_alpha: dict


def factor_agent_graph(llm):
    factor_node = FactorAgent(llm)

    graph = StateGraph(FactorAgentState)

    graph.add_node("generate_ast", factor_node.generate_ast)
    graph.add_node("execute_code", factor_node.execute_code)
    graph.add_node("final_output", factor_node.final_output)

    graph.add_edge(START, "generate_ast")
    graph.add_edge("generate_ast", "execute_code")
    graph.add_edge("execute_code", "final_output")
    graph.add_edge("final_output", END)

    factor_agent_graph = graph.compile()

    return factor_agent_graph
    

