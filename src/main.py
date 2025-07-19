from contextlib import asynccontextmanager
from datetime import datetime, timezone
import os
from uuid import uuid4
import bcrypt
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import Global
from src.databases.db import prisma
from src.controllers.index import index_router
from src.utils.types.UserProvider import UserAccountProvider, UserSecretProvider
from src.services.kis import KisService

Global.validate_env()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    print("✅ Prisma Connected")
    yield
    await prisma.disconnect()
    print("❌ Prisma Disconnected")


app = FastAPI(
    docs_url="/api-docs",
    lifespan=lifespan,
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app에 미리 만들어둔 index_router를 붙이는 것.
# app.include_router(index_router)

app.include_router(index_router)


@app.get("/")
def health_check():
    return {"message": "Hello World"}


# 초기 유저의 이메일은 user@example.com, 비밀번호는 string
async def user_info_init():

    not_created = []

    # 유저 생성
    # Hash password
    password = bcrypt.hashpw("string".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:

        user = await prisma.user.create(
            data={
                "name": "Test User",
                "email": "user@example.com",
                "password": password,
                "id": str(uuid4()),
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    except Exception as e:
        print(e)
        user = await prisma.user.find_unique(where={"email": "user@example.com"})
        not_created.append("user")
        pass

    user_id = user.id

    # 초기 계좌 생성
    try:
        await prisma.useraccount.create(
            data={
                "id": str(uuid4()),
                "user_id": user_id,
                "account": Global.env.KIS_ACCOUNT_NUMBER,
                "provider": UserAccountProvider.KIS,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
    except Exception as e:
        print(e)
        not_created.append("useraccount")
        pass

    # 초기 KIS Secret 값들 생성
    try:
        await prisma.usersecret.create(
            data={
                "id": str(uuid4()),
                "user_id": user_id,
                "value": Global.env.KIS_APP_KEY,
                "key": UserSecretProvider.KIS_APP_KEY,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )

        await prisma.usersecret.create(
            data={
                "id": str(uuid4()),
                "user_id": user_id,
                "value": Global.env.KIS_SECRET_KEY,
                "key": UserSecretProvider.KIS_SECRET_KEY,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
    except Exception as e:
        print(e)
        not_created.append("usersecret")
        pass

    await KisService().update_access_token(user_id)

    return not_created


@app.post("/user/init", tags=["__INIT__"])
async def user_init():
    return await user_info_init()


# @app.post("/idea/test")
# def read_idea():
#     return ideaAgent.test()


# class IdeaRequest(BaseModel):
#     messages: str


# @app.post("/idea")
# def read_idea(request: IdeaRequest):
#     return ideaAgent.invoke({"messages": [("user", request.messages)]})
