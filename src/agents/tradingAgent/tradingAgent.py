from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.services.kis import KisService
from src.config import Global
from src.agents.tradingAgent.prompt import TradingAgentPrompt
from typing import List
from langchain_core.tools import Tool
from langchain_core.messages import ToolCall


class TradingAgent:
    llm: ChatOpenAI
    llm_with_tools: ChatOpenAI
    system_prompt: str
    prompt_template: ChatPromptTemplate
    tools: List[Tool]

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=Global.env.OPENAI_API_KEY)
        self.system_prompt = TradingAgentPrompt.system_prompt
        self.prompt_template = ChatPromptTemplate.from_messages(
            [("system", self.system_prompt), ("human", "{input}")]
        )

        # Tool
        self.tools = [
            Tool(
                name="get_overseas_stock_daily_price",
                description=KisService.get_overseas_stock_daily_price.__doc__,
                func=KisService.get_overseas_stock_daily_price,
                args_schema=KisService.get_overseas_stock_daily_price.args_schema.model_json_schema(),
            )
        ]

        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def get_response(self, user_input: str) -> str:
        chain = self.prompt_template | self.llm_with_tools
        response = chain.invoke({"input": user_input})
        print(response.tool_calls)
        print("--------------------------------")
        print(response)
        print("--------------------------------")
        if len(response.tool_calls) > 0:
            res = self.execute_tool_call(response.tool_calls[0])
            print(res)
            return res
        return response.content

    def execute_tool_call(self, tool_call: ToolCall) -> str:
        tool_name = tool_call["name"]
        tool_input = tool_call["args"]
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if tool:
            print("=====================tool_input=======================")
            print(tool_input)
            print("=======================================================")
            return tool.func(tool_input)  # 핵심...!(?)
        return "Tool not found"
