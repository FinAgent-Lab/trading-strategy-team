import json
import requests
from src.config import Global


class KisService:
    _instance = None
    url: str
    fake_url: str

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # 초기화 코드 (한 번만 호출됨)
        if not hasattr(
            self, "_initialized"
        ):  # 이미 초기화된 경우는 다시 초기화하지 않음
            self._initialized = True
            self._data = {}
            self.url = "https://openapi.koreainvestment.com:9443"
            self.fake_url = "https://openapivts.koreainvestment.com:29443"

    def get_access_token(self):
        print(Global.env.KIS_APP_KEY)
        print(Global.env.KIS_SECRET_KEY)

        response = requests.post(
            url=f"{self.fake_url}/oauth2/tokenP",
            headers={
                "Content-Type": "application/json; charset=UTF-8",
            },
            data=json.dumps(
                {
                    "grant_type": "client_credentials",
                    "appkey": Global.env.KIS_APP_KEY,
                    "appsecret": Global.env.KIS_SECRET_KEY,
                }
            ),
        )

        body = response.json()

        return body["access_token"]
