from src.dtos.chat.chatDto import ChatListDto
from src.utils.types.PromptType import PromptType


def convertChatToPrompt(chats: list[ChatListDto] | list | list[PromptType]):
    try:
        return [{"role": chat["role"], "content": chat["content"]} for chat in chats]
    except:
        pass
    return [{"role": chat.role, "content": chat.content} for chat in chats]
