from enum import Enum


class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatAgent(str, Enum):
    HUMAN = "human"
    SYSTEM = "system"
    TRADE = "trade"
    IDEA = "idea"
    FACTOR = "factor"
    ANALYSIS = "analysis"
    EVALUATION = "evaluation"
