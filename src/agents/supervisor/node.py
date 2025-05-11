from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.agents.supervisor.state import SupervisorState
from src.dtos.chat.chatDto import CreateChatDto
from src.services.chat import ChatService
from src.utils.baseNode import BaseNode
from src.config import Global
from src.utils.functions.convertChatToPrompt import convertChatToPrompt
from src.utils.types.ChatType import ChatAgent, ChatRole
from src.utils.types.PromptType import PromptType


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
                "You are Trading Agent, a trading agent that helps users to trade stocks.",
                "You can analyze stock charts, generate hypothesis, analyze factors about trading like alpha factors, and perform trading.",
                "If user asks about you, respond with what you can do and who you are.",
                "You have 4 types of agents: chart-analysis, idea, factor, investment.",
                "<Agent List>",
                "You are a routing agent that classifies user input into one of the following.",
                "If user want to execute one of the agents, you never ask to user just execute it.",
                '1. "chart-analysis": a chart analysis agent that analyzes stock charts. When you want to trade stocks, you must start with this agent.',
                '2. "idea": an hypothesis agent that generates hypothesis. After "chart-analysis", you can use this agent to generate hypothesis.',
                '3. "factor": a factor agent that analyzes alpha factors or other factors about trading based on the hypothesis. After "idea", you can use this agent to analyze factors.',
                '4. "investment": an investment agent performs trading based on the factor or directly trading stocks. After "factor", you can use this agent to analyze investments.',
                "</Agent List>",
                # "",
                # '1. "chart-analysis" - when the user is asking for chart analysis. or asking for want to stock trading.',
                # '2. "idea" - when the user is proposing a new idea or concept, or asking for brainstorming. or chart analysis was successfully done.',
                # '3. "factor" - when the user is analyzing components, features, or evaluating pros and cons. or idea was successfully done.',
                # '4. "investment" - when the user is concerned with investment, ROI, monetization, or funding. or factor was successfully done.',
                "",
                "After you call one of the agents, you ask to user that they want to continue next agent or proceed automatically by yourself.",
                "If user wants to continue next agent, you return the next agent of <Agent List> in sequence. Return only one of: 'chart-analysis', 'idea', 'factor', 'investment', or 'etc'.",
                # "If user doesn't want to continue next agent, you end the conversation.",
                "If user wants to proceed automatically or leaves the decision to you, return the next agent of <Agent List> in sequence. Return only one of: 'chart-analysis', 'idea', 'factor', 'investment', or 'etc'.",
                "",
                "Given the user's message, decide which category it belongs to. Return only one of: 'chart-analysis', 'idea', 'factor', 'investment', or 'etc'. Do not explain. Do not include anything else.",
                "If the user's input does not match any of the categories, respond with polite message directly to the user with original input.",
                "When you response string, you must exclude the ' or \" from the response string.",
                "",
                "If Error occurs, respond with error message and why it occurs. If Error occurs, do not execute next agent.",
            ]
        )

        # self.prompt_template = ChatPromptTemplate.from_messages(
        #     [("system", self.system_prompt), ("human", "{messages}")]
        # )

    async def invoke(self, state: SupervisorState):

        history = convertChatToPrompt(state["common"]["history"])
        messages = convertChatToPrompt(state["common"]["messages"])

        prompt = (
            [
                {
                    "role": "system",
                    "content": self.system_prompt,
                }
            ]
            + history
            + messages
        )

        print(prompt)

        response = await self.llm.ainvoke(prompt)

        state["common"]["messages"].append(
            PromptType(
                role=ChatRole.ASSISTANT,
                content=response.content,
            )
        )

        return state
