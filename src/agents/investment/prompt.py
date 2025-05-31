import os
from src.agents.supervisor.state import State
from src.utils.functions.convertChatToPrompt import convertChatToPrompt
from src.utils.types.ChatType import ChatRole
from src.utils.types.PromptType import PromptType


try:
    with open(
        os.path.join(os.path.dirname(__file__), "../prompt/investment.md"),
        "r",
        encoding="utf-8",
    ) as f:
        system_prompt = f.read()
except FileNotFoundError:
    raise FileNotFoundError("investment.md not found")


def investment_prompt(state: State):
    prompt = [PromptType(role=ChatRole.SYSTEM, content=system_prompt)]

    return convertChatToPrompt(prompt)
