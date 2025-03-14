from fastapi import FastAPI
from src.config import Global
from src.contorllers.index import index_router

app = FastAPI(
    docs_url="/api-docs",
)

app.include_router(index_router)

Global.validate_env()

print(Global.env.DATABASE_URL)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
