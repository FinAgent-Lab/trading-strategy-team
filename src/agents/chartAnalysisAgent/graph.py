from langgraph.graph import StateGraph, START, END
from src.agents.chartAnalysisAgent.state import ChartAnalysisState
from src.agents.chartAnalysisAgent.node import (
    get_stock_data,
    describe_columns,
    analyze_chart,
    predict_future,
    plot_chart,
    summarize_results
)


# LangGraph Workflow 구성
def create_chart_analysis_graph():
    workflow = StateGraph(ChartAnalysisState)
    
    # 노드 추가
    workflow.add_node("get_stock_data", get_stock_data)
    workflow.add_node("describe_columns", describe_columns)
    workflow.add_node("analyze_chart", analyze_chart)
    workflow.add_node("predict_future", predict_future)
    workflow.add_node("plot_chart", plot_chart)
    workflow.add_node("summarize_results", summarize_results)
    
    # Workflow 순서 설정
    workflow.set_entry_point("get_stock_data")
    workflow.add_edge("get_stock_data", "describe_columns")
    workflow.add_edge("describe_columns", "analyze_chart")
    workflow.add_edge("analyze_chart", "predict_future")
    workflow.add_edge("predict_future", "plot_chart")
    workflow.add_edge("plot_chart", "summarize_results")
    workflow.add_edge("summarize_results", END)
    
    return workflow.compile()


# 그래프 인스턴스 생성
chart_analysis_graph = create_chart_analysis_graph()