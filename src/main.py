import os
from pydantic import BaseModel
from fastapi import FastAPI
from src.config import Global
# from src.contorllers.index import index_router
from src.agents.ideaAgent.ideaAgent import IdeaAgent

Global.validate_env()

app = FastAPI(
    docs_url="/api-docs",
)

# app에 미리 만들어둔 index_router를 붙이는 것.
# app.include_router(index_router)

ideaAgent = IdeaAgent()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/idea/test")
def read_idea():
    return ideaAgent.test()

class IdeaRequest(BaseModel):
    messages: str

@app.post("/idea")
def read_idea(request: IdeaRequest):
    return ideaAgent.invoke({"messages": [("user", request.messages)]})
