from pydantic import BaseModel
from src.utils.types.UserProvider import UserAccountProvider


class CreateAccountDto(BaseModel):
    account: str
    provider: UserAccountProvider
