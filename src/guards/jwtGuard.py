from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from src.config import Global
from src.guards.jwt import JwtService

bearer_docs = APIKeyHeader(name="authorization", scheme_name="Bearer")


def jwt_guard(
    credentials: Annotated[str, Depends(bearer_docs)],
):
    token = credentials
    jwt_service = JwtService()
    # if access_token is None:
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    # [bearer, token] = access_token.split(" ")

    # if bearer != "Bearer":
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        payload = jwt_service.decode(token, Global.env.JWT_SECRET, "HS256")
        return payload["id"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
