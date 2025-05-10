import json
from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from src.dtos.chat.chatDto import CreateChatDto
from src.services.chat import ChatService
from src.agents.investment.state import InvestmentState
from src.config import Global
from src.utils.baseNode import BaseNode
from langchain_core.messages import ToolCall
from src.agents.tools.kisTool import (
    get_overseas_stock_daily_price,
    order_overseas_stock,
    book_overseas_stock_order,
    cancel_overseas_stock_order,
    get_overseas_stock_order_resv_list,
    update_access_token,
)
from src.utils.functions.convertChatToPrompt import convertChatToPrompt
from src.utils.types.ChatType import ChatAgent, ChatRole


class InvestmentNode(BaseNode):
    chat_service: ChatService

    def __init__(self, llm: ChatOpenAI | None = None):
        self.chat_service = ChatService()

        self.llm = (
            lambda: (
                llm
                if llm
                else ChatOpenAI(
                    model="gpt-4o-mini",
                    api_key=Global.env.OPENAI_API_KEY,
                )
            )
        )()
        self.system_prompt = "\n".join(
            [
                "Please respond in the same language as the user's input.",
                "You are a trading assistant AI. Your job is to understand the user's intent, decide if any tool should be executed, and respond accordingly.",
                "If a tool call is needed, call the appropriate tool with accurate arguments. Then, based on the result of the tool, either:",
                "- Return a final answer to the user, or",
                "- Decide if another tool should be called.",
                "You must never transform the tool result. Just forward the result or decide what to do next.",
                "Never call the same tool more than once. Always think twice before calling a tool.",
                "If you plan to call a tool, but some required arguments are missing:",
                "- First, check if the missing values can be obtained by calling another available tool.",
                "- If possible, call the necessary tool to obtain the missing values first, before asking the user.",
                "- Only if no tool can provide the missing values, you MUST ask the user for those missing values in the assistant's content message.",
                "Think one more time before calling a tool.",
                # "If you plan to execute a tool and all required arguments are present, DO NOT include any message in the assistant's content. Just return the tool call.",
                # "If you plan to execute a tool and some required arguments are missing, you MUST ask the user for those missing values in the assistant's content message.",
            ]
        )
        # self.prompt_template = ChatPromptTemplate.from_messages(
        #     [("system", self.system_prompt), ("human", "{messages}")]
        # )

        self.tools = [
            Tool(
                name=update_access_token.name,
                description=update_access_token.__doc__,
                func=update_access_token,
                coroutine=update_access_token.arun,
                args_schema=update_access_token.args_schema,
            ),
            # Tool(
            #     name=get_overseas_stock_daily_price.name,
            #     description=get_overseas_stock_daily_price.__doc__,
            #     func=get_overseas_stock_daily_price,
            #     coroutine=get_overseas_stock_daily_price.arun,
            #     args_schema=get_overseas_stock_daily_price.args_schema,
            # ),
            Tool(
                name=order_overseas_stock.name,
                description=order_overseas_stock.__doc__,
                func=order_overseas_stock,
                coroutine=order_overseas_stock.arun,
                args_schema=order_overseas_stock.args_schema,
            ),
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

    async def invoke(self, state: InvestmentState):
        room_id = state["common"]["room"]["id"]
        user_id = state["common"]["user"]["id"]

        chats = await self.chat_service.get_chat_list(room_id)

        history = convertChatToPrompt(chats["chats"])

        # print history
        print("--------------------------------history--------------------------------")

        for h in history:
            print(f"{h['role']}: {h['content']}")
        print("-----------------------------------------------------------------------")

        prompt = [
            {
                "role": "system",
                "content": "".join(
                    [
                        self.system_prompt,
                        "\n\n",
                        f"The user_id is {user_id}, room_id is {room_id}",
                    ]
                ),
            }
        ] + history

        messages = await self.llm_with_tools.ainvoke(prompt)

        print("\n\n----------------------messages-------------------------")
        print(messages)
        print("------------------------------------------------------\n\n")

        tool_call_results: list = []

        for tool_call in messages.tool_calls:
            # 발화로부터 인자 정보를 충분히 못 얻었을 경우 다시 물어보기 위한 로직
            if messages.content.strip() != "":
                print(f"save chat for tool call: {messages.content}")

                await self.chat_service.create_chat(
                    room_id,
                    user_id,
                    CreateChatDto(
                        content=messages.content,
                        role=ChatRole.ASSISTANT,
                        agent=ChatAgent.INVESTMENT,
                    ),
                )

                state["common"]["messages"].append(
                    {
                        "role": "assistant",
                        "content": messages.content,
                    }
                )

                return state
            try:
                state["common"]["messages"].append(
                    {
                        "role": "assistant",
                        "content": messages.model_dump_json(),
                    }
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
                state["common"]["messages"]
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
            print(f"save chat for tool call result: {tool_messages.content}")

            await self.chat_service.create_chat(
                room_id,
                user_id,
                CreateChatDto(
                    content=tool_messages.content,
                    role=ChatRole.ASSISTANT,
                    agent=ChatAgent.INVESTMENT,
                ),
            )

            state["common"]["messages"].append(
                {
                    "role": "assistant",
                    "content": tool_messages.content,
                }
            )

            return state

        print(f"save chat: {messages.content}")

        await self.chat_service.create_chat(
            room_id,
            user_id,
            CreateChatDto(
                content=messages.content,
                role=ChatRole.ASSISTANT,
                agent=ChatAgent.INVESTMENT,
            ),
        )

        state["common"]["messages"].append(
            {
                "role": "assistant",
                "content": messages.content,
            }
        )

        return state

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

                return await tool.coroutine(validated_args.model_dump())  # 핵심...!(?)
        except Exception as e:
            print(e.__str__())
            raise HTTPException(status_code=400, detail=e.__str__())

        return "Tool not found"
