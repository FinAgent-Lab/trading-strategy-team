from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.agents.supervisor.state import SupervisorState
from src.dtos.chat.chatDto import CreateChatDto
from src.services.chat import ChatService
from src.utils.baseNode import BaseNode
from src.config import Global
from src.utils.functions.convertChatToPrompt import convertChatToPrompt
from src.utils.types.ChatType import ChatAgent, ChatRole


class SupervisorNode(BaseNode):
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

        self.system_prompt = "\n".join(
            [
                "You are a routing agent that classifies user input into one of the following categories:",
                "",
                '1. "idea" - when the user is proposing a new idea or concept, or asking for brainstorming.',
                '2. "factor" - when the user is analyzing components, features, or evaluating pros and cons.',
                '3. "invest" - when the user is concerned with investment, ROI, monetization, or funding.',
                "",
                'Given the user\'s message, decide which category it belongs to. Return only one of: "idea", "factor", "invest", or "etc". Do not explain. Do not include anything else.',
                "If the user's input does not match any of the categories, respond with a short and polite message directly to the user.",
            ]
        )

        # self.prompt_template = ChatPromptTemplate.from_messages(
        #     [("system", self.system_prompt), ("human", "{messages}")]
        # )

    async def invoke(self, state: SupervisorState):
        room_id = state["room_id"]
        user_id = state["user_id"]
        input = str(state["messages"][-1].content)
        print()

        chats = await self.chat_service.get_chat_list(room_id)

        history = convertChatToPrompt(chats["chats"])

        prompt = (
            [
                {
                    "role": "system",
                    "content": self.system_prompt,
                }
            ]
            + history
            + [{"role": "user", "content": input}]
        )

        response = await self.llm.ainvoke(prompt)

        print(f"Supervisor response: {response.content}")

        await self.chat_service.create_chat(
            room_id,
            user_id,
            CreateChatDto(
                content=response.content,
                role=ChatRole.ASSISTANT,
                agent=ChatAgent.SUPERVISOR,
            ),
        )

        return {"messages": [response]}
