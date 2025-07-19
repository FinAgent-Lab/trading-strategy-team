from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from src.agents.factor.node import FactorAgent
from src.agents.supervisor.state import SupervisorState
from src.config import Global


def factor_agent_graph(llm: ChatOpenAI | None = None):
    llm = llm if llm else ChatOpenAI(model="gpt-4.1", api_key=Global.env.OPENAI_API_KEY)

    factor_node = FactorAgent(llm)

    graph = StateGraph(SupervisorState)

    graph.add_node("generate_ast", factor_node.generate_ast)
    graph.add_node("execute_code", factor_node.execute_code)
    graph.add_node("final_output", factor_node.final_output)
    graph.add_node("rebalance_value_node", factor_node.rebalance_value)
    graph.add_node("rebalance_shares_node", factor_node.rebalance_shares)

    graph.add_edge(START, "generate_ast")
    graph.add_edge("generate_ast", "execute_code")
    graph.add_edge("execute_code", "final_output")
    graph.add_edge("final_output", "rebalance_value_node")
    graph.add_edge("rebalance_value_node", "rebalance_shares_node")
    graph.add_edge("rebalance_shares_node", END)

    factor_agent_graph = graph.compile()

    return factor_agent_graph
