from langchain_openai import ChatOpenAI
from src.agents.supervisor.prompt import supervisor_prompt
from src.agents.supervisor.state import State
from src.utils.baseNode import BaseNode
from src.config import Global
from src.utils.functions.convertChatToPrompt import convertChatToPrompt
from src.utils.types.ChatType import ChatRole
from src.utils.types.PromptType import PromptType


class SupervisorNode(BaseNode):
    def __init__(self, llm: ChatOpenAI | None = None):

        self.llm = (
            llm
            if llm
            else ChatOpenAI(
                model="gpt-4o-mini",
                api_key=Global.env.OPENAI_API_KEY,
            )
        )

        self.system_prompt = supervisor_prompt

    async def invoke(self, state: State):

        history = convertChatToPrompt(state["common"]["histories"])
        messages = convertChatToPrompt(state["common"]["messages"])

        # # history & messages
        # PromptType(role=ChatRole.USER, content="Hello")

        # # convert
        # {"role": "user", "content": "Hello"}

        print("Supervisor Node Messages:")
        print(messages[-1]["content"])
        print()

        prompt = self.system_prompt(state) + history + messages

        response = await self.llm.ainvoke(prompt)

        print("Supervisor Node Prompt:")
        print(prompt)
        print()
        print("Supervisor Node Response:")
        print(response)
        print()

        cleaned_content = response.content.strip().strip('"').strip("'")

        print(f"Supervisor Node response: {response.content}")
        print()

        state["common"]["messages"].append(
            PromptType(
                role=ChatRole.ASSISTANT,
                content=cleaned_content,
            )
        )

        return state
