from pydantic import BaseModel


class CreateRoomDto(BaseModel):
    name: str | None = None
