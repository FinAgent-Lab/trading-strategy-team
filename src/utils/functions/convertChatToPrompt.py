def convertChatToPrompt(chats: list):
    return [{"role": chat["role"], "content": chat["content"]} for chat in chats]
