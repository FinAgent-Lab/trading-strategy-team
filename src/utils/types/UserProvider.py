from enum import Enum


class UserSecretProvider(str, Enum):
    KIS_APP_KEY = "KIS_APP_KEY"
    KIS_SECRET_KEY = "KIS_SECRET_KEY"
    KIS_ACCESS_TOKEN = "KIS_ACCESS_TOKEN"


class UserAccountProvider(str, Enum):
    KIS = "KIS"
