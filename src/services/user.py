from typing_extensions import Self
from src.dtos.user.accountDto import CreateAccountDto
from src.config import Global
from src.guards.jwt import JwtService
from src.dtos.user.signDto import SignInDto, SignUpDto
from src.dtos.user.secretDto import CreateSecretDto
from src.databases.db import prisma
from datetime import datetime, timezone
from fastapi import HTTPException
from uuid import uuid4
import bcrypt


class UserService:
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

    async def sign_up(self, input: SignUpDto):
        exist_user = await prisma.user.find_unique(where={"email": input.email})

        if exist_user:
            raise HTTPException(
                status_code=404, detail="User Already Exist. Please Change Email."
            )

        # Hash password
        input.password = bcrypt.hashpw(
            input.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user = await prisma.user.create(
            data={
                **input.model_dump(),
                "id": str(uuid4()),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

        return {"email": user.email, "name": user.name}

    async def sign_in(self, input: SignInDto):
        user = await prisma.user.find_unique(
            where={"email": input.email, "deleted_at": None}
        )

        if not user:
            raise HTTPException(status_code=404, detail="Bad Request Exception.")

        # Validate password
        if not bcrypt.checkpw(
            input.password.encode("utf-8"), user.password.encode("utf-8")
        ):
            raise HTTPException(status_code=404, detail="Bad Request Exception.")

        jwt_service = JwtService()
        token = jwt_service.encode(
            payload={"email": user.email, "id": user.id},
            secret=Global.env.JWT_SECRET,
            algorithm="HS256",
        )

        return {"email": user.email, "name": user.name, "access_token": token}

    async def get_own_info(self, user_id: str):
        user = await prisma.user.find_unique(where={"id": user_id, "deleted_at": None})

        if not user:
            raise HTTPException(status_code=404, detail="User Not Found.")

        return {
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at,
        }

    async def create_secret(self, input: CreateSecretDto, user_id: str) -> bool:
        await prisma.usersecret.create(
            data={
                "id": str(uuid4()),
                "user_id": user_id,
                "value": input.value,
                "key": input.key,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

        return True

    async def update_secret(self, input: CreateSecretDto, user_id: str) -> bool:
        await prisma.usersecret.update(
            where={
                "key_user_id": {
                    "key": input.key,
                    "user_id": user_id,
                },
                "deleted_at": None,
            },
            data={
                "value": input.value,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
        )

        return True

    async def get_secret_list(self, user_id: str):
        secrets = await prisma.usersecret.find_many(
            where={"user_id": user_id, "deleted_at": None}
        )

        return {
            "secrets": list(
                map(
                    lambda secret: {
                        "value": secret.value,
                        "key": secret.key,
                    },
                    secrets,
                )
            )
        }

    async def create_account(self, input: CreateAccountDto, user_id: str) -> bool:
        await prisma.useraccount.create(
            data={
                "id": str(uuid4()),
                "user_id": user_id,
                "account": input.account,
                "provider": input.provider,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

        return True

    async def get_account_list(self, user_id: str):
        accounts = await prisma.useraccount.find_many(
            where={"user_id": user_id, "deleted_at": None}
        )

        return {
            "accounts": list(
                map(
                    lambda account: {
                        "account": account.account,
                        "provider": account.provider,
                    },
                    accounts,
                )
            ),
        }
