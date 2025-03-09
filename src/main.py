from fastapi import FastAPI
from src.config import Global

app = FastAPI(
    docs_url="/api-docs",
)

Global.validate_env()

print(Global.env.DATABASE_URL)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
