import json
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from src.services.kis import KisService
from src.agents.tradeAgent.state import TradeState
from src.config import Global
from src.utils.baseNode import BaseNode
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolCall


class TradeNode(BaseNode):
    def __init__(self, llm: ChatOpenAI | None = None):
        self.llm = (
            lambda: (
                llm
                if llm
                else ChatOpenAI(model="gpt-4o-mini", api_key=Global.env.OPENAI_API_KEY)
            )
        )()
        self.system_prompt = "\n".join(
            [
                "You have to figure out the intentions of the user's speech, select the appropriate tool, and execute it. If you decide that you don't need to run the tool anymore, please return the appropriate response to the user based on the result.",
                "Don't run the tool you ran once again.",
                "Don't transform the result of the tool calling.",
            ]
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [("system", self.system_prompt), ("human", "{messages}")]
        )
        self.tools = [
            Tool(
                name="get_overseas_stock_daily_price",
                description=KisService.get_overseas_stock_daily_price.__doc__,
                func=KisService.get_overseas_stock_daily_price,
                args_schema=KisService.get_overseas_stock_daily_price.args_schema.model_json_schema(),
            ),
            Tool(
                name="get_access_token",
                description=KisService.get_access_token.__doc__,
                func=KisService.get_access_token,
                args_schema=KisService.get_access_token.args_schema.model_json_schema(),
            ),
        ]

        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def invoke(self, state: TradeState):
        prompt = [{"role": "system", "content": self.system_prompt}] + state["messages"]

        messages = self.llm_with_tools.invoke(prompt)

        print("\n\n----------------------messages-------------------------")
        print(messages)
        print("------------------------------------------------------\n\n")
        if len(messages.tool_calls) > 0:
            res = self.execute_tool_call(messages.tool_calls[0])

            print("---------------res--------------")
            print(res)
            print("--------------------------------")

            return {
                "messages": [json.dumps(res)],
                "processed": [
                    json.dumps({"tool_call": messages.tool_calls[0]["name"]})
                ],
            }

        print("content")
        return {"messages": [messages.content], "processed": ["content"]}

    def execute_tool_call(self, tool_call: ToolCall) -> str:
        tool_name = tool_call["name"]
        tool_input = tool_call["args"]
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if tool:
            print("\n\n=====================tool_input========================")
            print(tool_input)
            print("=======================================================\n\n")
            return tool.func(tool_input)  # 핵심...!(?)
        return "Tool not found"
