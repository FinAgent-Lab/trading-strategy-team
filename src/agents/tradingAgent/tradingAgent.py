from typing import Any, Dict, List
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from src.config import Global
from langgraph.graph import END, StateGraph
from src.agents.tradingAgent.prompt import TradingAgentPrompt


class TradingAgent:
    llm: ChatOpenAI
    system_prompt: str
    prompt_template: ChatPromptTemplate

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=Global.env.OPENAI_API_KEY)
        self.system_prompt = TradingAgentPrompt.system_prompt
        self.prompt_template = ChatPromptTemplate.from_messages(
            [("system", self.system_prompt), ("human", "{input}")]
        )

    def get_response(self, user_input: str) -> str:
        chain = self.prompt_template | self.llm
        response = chain.invoke({"input": user_input})
        return response.content
