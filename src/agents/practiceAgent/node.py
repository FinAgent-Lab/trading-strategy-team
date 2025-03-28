from langchain_openai import ChatOpenAI

from src.agents.practiceAgent.state import State
from src.config import Global

llm = ChatOpenAI(model="gpt-4o-mini", api_key=Global.env.OPENAI_API_KEY)


# Node
# 현재 State를 입력받아 messages라는 키 아래에 업데이트된 messages 목록을 포함하는 TypedDict를 반환.
def chatbot(state: State) -> State:
    return {"messages": [llm.invoke(state["messages"])]}
