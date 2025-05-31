from typing import Annotated, TypedDict
from src.utils.types.PromptType import PromptType


class CommonState(TypedDict):
    histories: Annotated[list[PromptType], "total chat histories in the room"]
    messages: Annotated[list[PromptType], "short term messages"]
    access_token: Annotated[str, "access_token"]
    account: Annotated[str, "account"]
