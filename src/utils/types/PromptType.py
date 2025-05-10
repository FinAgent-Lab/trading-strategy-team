from typing import Annotated
from pydantic import BaseModel

from src.utils.types.ChatType import ChatRole


class PromptType(BaseModel):
    role: Annotated[ChatRole, "role"]
    content: Annotated[str, "content"]
