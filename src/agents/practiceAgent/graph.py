from src.agents.practiceAgent.state import State
from langgraph.graph import StateGraph, START, END
from src.agents.practiceAgent.node import chatbot

# 그래프 생성
graph_builder = StateGraph(State)

# 노드 이름, 함수 혹은 callable 객체를 인자로 받아 노드를 추가
graph_builder.add_node("chatbot", chatbot)


# 그래프의 시작 노드에서 챗붓 노드로의 엣지 추가
graph_builder.add_edge(START, "chatbot")

# 챗붓 노드에서 그래프의 끝 노드로의 엣지 추가
graph_builder.add_edge("chatbot", END)

# 그래프 컴파일
graph = graph_builder.compile()

# # 그래프 실행
# question = "서울의 유명한 맛집 TOP 10 추천해줘."

# for event in graph.stream(
#     {"hihi": [("user", question)], "messages": [("user", "안녕하세요.")]}
# ):
#     # 이벤트 값 출력
#     for value in event.values():
#         print("Assistant:", value["messages"][-1].content)
