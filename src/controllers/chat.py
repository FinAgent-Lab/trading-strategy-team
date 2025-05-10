from fastapi import APIRouter, Depends, Path
from src.services.chat import ChatService
from src.guards.jwtGuard import jwt_guard
from typing import Annotated
from src.dtos.chat.roomDto import CreateRoomDto

chat_router = router = APIRouter()


@router.post("/room")
async def create_room(
    room_name: CreateRoomDto,
    user_id: Annotated[str, Depends(jwt_guard)],
    chat_service: ChatService = Depends(lambda: ChatService()),
):
    return await chat_service.create_room(room_name.name, user_id)


@router.get("/room/list")
async def get_room_list(
    user_id: Annotated[str, Depends(jwt_guard)],
    chat_service: ChatService = Depends(lambda: ChatService()),
):
    return await chat_service.get_room_list(user_id)


@router.get("/room/{room_id}/list")
async def get_chat_list(
    room_id: Annotated[str, Path()],
    user_id: Annotated[str, Depends(jwt_guard)],
    chat_service: ChatService = Depends(lambda: ChatService()),
):
    return await chat_service.get_chat_list(room_id)
