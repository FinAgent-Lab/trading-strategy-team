from typing import Annotated
from fastapi import APIRouter, Depends
from src.dtos.user.accountDto import CreateAccountDto
from src.guards.jwtGuard import jwt_guard
from src.services.user import UserService
from src.dtos.user.signDto import SignInDto, SignUpDto
from src.dtos.user.secretDto import CreateSecretDto

user_router = router = APIRouter()


@router.post("/sign-up")
async def sign_up(
    body: SignUpDto, user_service: UserService = Depends(lambda: UserService())
):
    print(body)
    return await user_service.sign_up(body)


@router.post("/sign-in")
async def sign_in(
    body: SignInDto, user_service: UserService = Depends(lambda: UserService())
):
    return await user_service.sign_in(body)


@router.get("/info")
async def get_own_info(
    user_id: Annotated[str, Depends(jwt_guard)],
    user_service: UserService = Depends(lambda: UserService()),
):
    return await user_service.get_own_info(user_id)


@router.post("/secret")
async def create_secret(
    body: CreateSecretDto,
    user_id: Annotated[str, Depends(jwt_guard)],
    user_service: UserService = Depends(lambda: UserService()),
) -> bool:
    return await user_service.create_secret(body, user_id)


@router.put("/secret")
async def update_secret(
    body: CreateSecretDto,
    user_id: Annotated[str, Depends(jwt_guard)],
    user_service: UserService = Depends(lambda: UserService()),
) -> bool:
    return await user_service.update_secret(body, user_id)


@router.get("/secret/list")
async def get_secret_list(
    user_id: Annotated[str, Depends(jwt_guard)],
    user_service: UserService = Depends(lambda: UserService()),
) -> dict:
    return await user_service.get_secret_list(user_id)


@router.post("/account")
async def create_account(
    body: CreateAccountDto,
    user_id: Annotated[str, Depends(jwt_guard)],
    user_service: UserService = Depends(lambda: UserService()),
) -> bool:
    return await user_service.create_account(body, user_id)


@router.get("/account/list")
async def get_account_list(
    user_id: Annotated[str, Depends(jwt_guard)],
    user_service: UserService = Depends(lambda: UserService()),
) -> dict:
    return await user_service.get_account_list(user_id)
