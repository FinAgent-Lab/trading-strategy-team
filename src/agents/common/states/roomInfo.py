from typing import TypedDict, Annotated


class RoomInfo(TypedDict):
    id: Annotated[str, "room id"]
