from typing_extensions import Self
from src.dtos.chat.chatDto import CreateChatDto
from src.databases.db import prisma
from uuid import uuid4
from datetime import datetime, timezone


class ChatService:
    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # 초기화 코드 (한 번만 호출됨)
        if not hasattr(
            self, "_initialized"
        ):  # 이미 초기화된 경우는 다시 초기화하지 않음
            self._initialized = True

    async def create_room(self, room_name: str | None, user_id: str):
        return await prisma.room.create(
            data={
                "id": str(uuid4()),
                "name": room_name if room_name else "New Chat",
                "user_id": user_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    async def get_room_list(self, user_id: str):
        rooms = await prisma.room.find_many(
            where={
                "user_id": user_id,
                "deleted_at": None,
            },
            order={"created_at": "desc"},
        )

        return {
            "rooms": list(
                map(
                    lambda room: {
                        "id": room.id,
                        "name": room.name,
                        "created_at": room.created_at,
                    },
                    rooms,
                )
            ),
        }

    async def get_chat_list(self, room_id: str):
        chats = await prisma.chat.find_many(
            where={
                "room_id": room_id,
                "deleted_at": None,
            },
            order={"created_at": "asc"},
        )

        return {
            "chats": list(
                map(
                    lambda chat: {
                        "id": chat.id,
                        "content": chat.content,
                        "role": chat.role,
                        "agent": chat.agent,
                        "created_at": chat.created_at,
                    },
                    chats,
                )
            ),
        }

    async def create_chat(self, room_id: str, user_id: str, input: CreateChatDto):

        return await prisma.chat.create(
            data={
                "id": str(uuid4()),
                "room_id": room_id,
                "user_id": user_id,
                "content": input.content,
                "role": input.role,
                "agent": input.agent,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
