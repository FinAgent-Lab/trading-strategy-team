from typing import TypedDict, Annotated


class UserInfo(TypedDict):
    id: Annotated[str, "user id"]
    account_number: Annotated[str, "account number"]
    access_token: Annotated[str, "access token"]
    app_key: Annotated[str, "app key"]
    app_secret: Annotated[str, "app secret"]
