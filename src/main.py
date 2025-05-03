from contextlib import asynccontextmanager
import os
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import Global
from src.agents.ideaAgent.ideaAgent import IdeaAgent
from src.databases.db import prisma
from src.controllers.index import index_router

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

ideaAgent = IdeaAgent()

app.include_router(index_router)

@app.get("/")
def health_check():
    return {"message": "Hello World"}

@app.post("/idea/test")
def read_idea():
    return ideaAgent.test()

class IdeaRequest(BaseModel):
    messages: str

@app.post("/idea")
def read_idea(request: IdeaRequest):
    return ideaAgent.invoke({"messages": [("user", request.messages)]})
