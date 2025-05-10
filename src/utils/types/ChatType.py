from enum import Enum


class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatAgent(str, Enum):
    HUMAN = "human"
    SYSTEM = "system"
    INVESTMENT = "investment"
    IDEA = "idea"
    FACTOR = "factor"
    EVALUATION = "evaluation"
    SUPERVISOR = "supervisor"
