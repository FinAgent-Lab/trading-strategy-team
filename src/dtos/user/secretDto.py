from pydantic import BaseModel

from src.utils.types.UserProvider import UserSecretProvider


class CreateSecretDto(BaseModel):
    key: UserSecretProvider
    value: str
