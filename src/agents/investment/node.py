import json
from fastapi import HTTPException
from langchain_core.messages import AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from src.agents.investment.prompt import investment_prompt
from src.agents.supervisor.state import State
from src.services.chat import ChatService
from src.config import Global
from src.utils.baseNode import BaseNode
from langchain_core.messages import ToolCall, BaseMessage
from src.agents.tools.kisTool import (
    get_overseas_stock_daily_price,
    order_overseas_stock,
    book_overseas_stock_order,
    cancel_overseas_stock_order,
    get_overseas_stock_order_resv_list,
)
from src.utils.functions.convertChatToPrompt import convertChatToPrompt
from src.utils.types.ChatType import ChatRole
from src.utils.types.PromptType import PromptType


class InvestmentNode(BaseNode):
    chat_service: ChatService

    def __init__(self, llm: ChatOpenAI | None = None):
        self.chat_service = ChatService()

        self.llm = (
            llm
            if llm
            else ChatOpenAI(
                model="gpt-4o-mini",
                api_key=Global.env.OPENAI_API_KEY,
            )
        )
        self.system_prompt = investment_prompt

        self.tools = [
            # Tool(
            #     name=get_overseas_stock_daily_price.name,
            #     description=get_overseas_stock_daily_price.__doc__,
            #     func=get_overseas_stock_daily_price,
            #     coroutine=get_overseas_stock_daily_price.arun,
            #     args_schema=get_overseas_stock_daily_price.args_schema,
            # ),
            order_overseas_stock,
            # Tool(
            #     name=book_overseas_stock_order.name,
            #     description=book_overseas_stock_order.__doc__,
            #     func=book_overseas_stock_order,
            #     coroutine=book_overseas_stock_order.arun,
            #     args_schema=book_overseas_stock_order.args_schema,
            # ),
            # Tool(
            #     name=cancel_overseas_stock_order.name,
            #     description=cancel_overseas_stock_order.__doc__,
            #     func=cancel_overseas_stock_order,
            #     coroutine=cancel_overseas_stock_order.arun,
            #     args_schema=cancel_overseas_stock_order.args_schema,
            # ),
            # Tool(
            #     name=get_overseas_stock_order_resv_list.name,
            #     description=get_overseas_stock_order_resv_list.__doc__,
            #     func=get_overseas_stock_order_resv_list,
            #     coroutine=get_overseas_stock_order_resv_list.arun,
            #     args_schema=get_overseas_stock_order_resv_list.args_schema,
            # ),
        ]

        self.llm_with_tools = self.llm.bind_tools(self.tools)

    async def invoke(self, state: State):
        history = convertChatToPrompt(
            state["common"]["histories"]
        ) + convertChatToPrompt(state["common"]["messages"])

        prompt = [
            *self.system_prompt(state),
            {
                "role": "system",
                "content": "".join(
                    [
                        f"Access Token: {state['common']['access_token']}",
                        "",
                        f"Account: {state['common']['account']}",
                    ]
                ),
            },
        ] + history

        messages = await self.llm_with_tools.ainvoke(prompt)

        print("\n\n----------------------messages-------------------------")
        print(messages)
        print("------------------------------------------------------\n\n")

        response = await self.process_response(messages)

        print("Investment Node Response:")
        print(response.content)
        print()

        if isinstance(response, list):
            for tool_message in response:
                state["common"]["messages"].append(
                    PromptType(
                        role=ChatRole.ASSISTANT,
                        content=tool_message.content,
                    )
                )

            return state

        state["common"]["messages"].append(
            PromptType(
                role=ChatRole.ASSISTANT,
                content=response.content,
            )
        )

        return state

        tool_call_results: list = []

        for tool_call in messages.tool_calls:
            # 발화로부터 인자 정보를 충분히 못 얻었을 경우 다시 물어보기 위한 로직
            if messages.content.strip() != "":
                print(f"save chat for tool call: {messages.content}")

                state["common"]["messages"].append(
                    PromptType(
                        role=ChatRole.ASSISTANT,
                        content=messages.content,
                    )
                )

                return state
            try:
                state["common"]["messages"].append(
                    PromptType(
                        role=ChatRole.ASSISTANT,
                        content=messages.model_dump_json(),
                    )
                )

                res = await self.execute_tool_call(tool_call)

                print("---------------res--------------")
                print(res)
                print("--------------------------------")

                tool_call_results.append(json.dumps(res))
            except Exception as e:
                raise HTTPException(status_code=400, detail=e.__str__())
                # print("error")
                # print(e.__str__())
                # error_message = await self.llm.ainvoke(
                #     state["messages"]
                #     + [
                #         {
                #             "role": "system",
                #             "content": "".join(
                #                 [
                #                     "Please modify this message clearly and deliver it to the user.",
                #                     "You must respond in the same language as the user's input.(Normally Korean)",
                #                     "The message is: ",
                #                     e.__str__(),
                #                 ]
                #             ),
                #         },
                #     ]
                # )
                # return {"messages": [error_message.content]}

        # 툴 호출 결과가 있을 경우, 응답을 가공해서 response
        if len(tool_call_results) > 0:
            tool_messages = await self.llm_with_tools.ainvoke(
                convertChatToPrompt(state["common"]["messages"])
                + [
                    {
                        "role": "assistant",
                        "content": "\n".join(tool_call_results),
                    }
                ]
                + [
                    {
                        "role": "user",
                        "content": "Please analyze the tool call results and provide a final answer to the user.",
                    }
                ]
            )
            print(f"Investment chat for tool call result: {tool_messages.content}")

            state["common"]["messages"].append(
                PromptType(
                    role=ChatRole.ASSISTANT,
                    content=tool_messages.content,
                )
            )

            return state

        print(f"Investment chat: {messages.content}")

        state["common"]["messages"].append(
            PromptType(
                role=ChatRole.ASSISTANT,
                content=messages.content,
            )
        )

        return state

    async def process_response(self, message: BaseMessage):
        print(f"Tool Calls: {message.tool_calls}")

        tool_call_results: list[ToolMessage] = []

        for tool_call in message.tool_calls:
            res = await self.execute_tool_call(tool_call)
            tool_call_results.append(
                ToolMessage(
                    content=json.dumps(res),
                    tool_call_id=tool_call["id"],
                    name=tool_call["name"],
                )
            )
            print(
                ToolMessage(
                    content=json.dumps(res),
                    tool_call_id=tool_call["id"],
                    name=tool_call["name"],
                )
            )

        if len(tool_call_results) > 0:
            return tool_call_results

        return message

    async def execute_tool_call(self, tool_call: ToolCall):
        tool_name = tool_call["name"]
        tool_input = tool_call["args"]
        tool = next((t for t in self.tools if t.name == tool_name), None)

        try:
            if tool:
                print("\n\n=====================tool_input========================")
                print(tool_name)
                print(tool_input)
                print("=======================================================\n\n")

                validated_args = tool.args_schema.model_validate(tool_input)

                print("validated_args")
                print(validated_args.model_dump())

                return await tool.coroutine(validated_args.input)  # 핵심...!(?)
        except Exception as e:
            print(e.__str__())
            raise HTTPException(status_code=400, detail=e.__str__())

        return "Tool not found"
