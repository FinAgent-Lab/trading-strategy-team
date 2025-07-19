from datetime import datetime, timezone
import json
import uuid
from fastapi import HTTPException
import requests
from src.dtos.kis.tradeDto import TradeDto
from src.config import Global
from src.utils.constants.trId import TRADE_ID
from src.databases.db import prisma
from src.utils.types.UserProvider import UserAccountProvider, UserSecretProvider


class KisService:
    _instance = None
    url: str

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

            # self.url = "https://openapi.koreainvestment.com:9443"  # 실전 투자 url

            self.url = "https://openapivts.koreainvestment.com:29443"  # 모의 투자 url

    async def get_access_token(self, user_id: str) -> str:
        """
        KIS 액세스 토큰 발급
        """

        access_token = await prisma.usersecret.find_unique(
            where={
                "key_user_id": {
                    "key": UserSecretProvider.KIS_ACCESS_TOKEN,
                    "user_id": user_id,
                },
                "deleted_at": None,
            },
        )

        if access_token:
            updated_at = datetime.fromisoformat(access_token.updated_at.isoformat())
            now = datetime.now(timezone.utc)
            hours_diff = (now - updated_at).total_seconds() / 3600

            if hours_diff >= 12:
                return await self.update_access_token(user_id)

        return (
            access_token.value
            if access_token
            else await self.update_access_token(user_id)
        )

    async def update_access_token(self, user_id: str) -> str:
        kis_app_key = await prisma.usersecret.find_unique(
            where={
                "key_user_id": {
                    "key": UserSecretProvider.KIS_APP_KEY,
                    "user_id": user_id,
                },
            },
        )

        kis_secret_key = await prisma.usersecret.find_unique(
            where={
                "key_user_id": {
                    "key": UserSecretProvider.KIS_SECRET_KEY,
                    "user_id": user_id,
                },
            },
        )

        if not kis_app_key:
            raise HTTPException(
                status_code=400, detail="KIS 앱 키가 존재하지 않습니다."
            )

        if not kis_secret_key:
            raise HTTPException(
                status_code=400, detail="KIS 시크릿 키가 존재하지 않습니다."
            )

        response = requests.post(
            url=f"{self.url}/oauth2/tokenP",
            headers={
                "Content-Type": "application/json; charset=UTF-8",
            },
            data=json.dumps(
                {
                    "grant_type": "client_credentials",
                    "appkey": kis_app_key.value,
                    "appsecret": kis_secret_key.value,
                }
            ),
        )

        body = response.json()

        if type(body) == str:
            raise HTTPException(status_code=400, detail="KIS 액세스 토큰 발급 실패")

        print("update access token")
        print(user_id)
        print("body")
        print(body)

        await prisma.usersecret.upsert(
            where={
                "key_user_id": {
                    "key": UserSecretProvider.KIS_ACCESS_TOKEN,
                    "user_id": user_id,
                },
            },
            data={
                "create": {
                    "id": str(uuid.uuid4()),
                    "key": UserSecretProvider.KIS_ACCESS_TOKEN,
                    "value": body["access_token"],
                    "user_id": user_id,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                },
                "update": {
                    "value": body["access_token"],
                },
            },
        )

        return body["access_token"]

    async def get_overseas_stock_daily_price(
        self,
        input: TradeDto.GetOverseasStockDailyPriceInput,
    ) -> TradeDto.GetOverseasStockDailyPriceOutput:
        """
        해외 주식 기간별 시세
        """

        access_token = await self.get_access_token(input.user_id)

        try:
            response = requests.get(
                url=f"{self.url}/uapi/overseas-price/v1/quotations/dailyprice",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "appkey": Global.env.KIS_APP_KEY,
                    "appsecret": Global.env.KIS_SECRET_KEY,
                    "tr_id": "HHDFS76240000",
                },
                params=input.model_dump(),
            )

            # print(f"📌 요청 URL: {response.self.url}")
            # print(f"🔹 응답 코드: {response.status_code}")
            # print(f"🔹 응답 내용: {response.text}")

            body: TradeDto.GetOverseasStockDailyPriceOutput = response.json()

            return body
        except Exception as e:
            print(e)
            raise e

    async def order_overseas_stock(
        self,
        input: TradeDto.OrderOverseasStockInput,
    ) -> dict:
        """
        해외 주식 주문
        """

        trade = TRADE_ID["usa"]["buy"] if input.is_buy else TRADE_ID["usa"]["sell"]

        access_token = await self.get_access_token(input.user_id)

        account = await prisma.useraccount.find_first(
            where={
                "user_id": input.user_id,
                "provider": UserAccountProvider.KIS,
                "deleted_at": None,
            },
        )

        payload = input.model_dump()
        del payload["user_id"]
        del payload["is_buy"]

        payload["CANO"] = account.account

        print(f"🔹 payload: {payload}")
        print(f"🔹 trade: {trade}")

        if not account:
            raise HTTPException(status_code=400, detail="KIS 계좌가 존재하지 않습니다.")

        try:
            response = requests.post(
                url=f"{self.url}/uapi/overseas-stock/v1/trading/order",
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {access_token}",
                    "appkey": Global.env.KIS_APP_KEY,
                    "appsecret": Global.env.KIS_SECRET_KEY,
                    "tr_id": trade,
                },
                json=payload,
            )

            return response.json()
        except Exception as e:
            print(e)
            raise e

    async def book_overseas_stock_order(
        self,
        input: TradeDto.BookOverseasStockOrderInput,
    ):
        """
        해외 주식 주문 예약
        """

        trade = TRADE_ID["usa"]["buy"] if input.is_buy else TRADE_ID["usa"]["sell"]

        access_token = await self.get_access_token(input.user_id)

        try:
            response = requests.post(
                url=f"{self.url}/uapi/overseas-stock/v1/trading/order-resv",
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {access_token}",
                    "appkey": Global.env.KIS_APP_KEY,
                    "appsecret": Global.env.KIS_SECRET_KEY,
                    "tr_id": trade,
                },
                data=input.model_dump_json(),
            )

            return response.json()
        except Exception as e:
            print(e)
            raise e

    async def cancel_overseas_stock_order(
        self,
        input: TradeDto.CancelOverseasStockOrderInput,
    ):
        """
        해외 주식 주문 취소
        """

        trade = TRADE_ID["usa"]["book_cancel"]

        access_token = await self.get_access_token(input.user_id)

        try:
            response = requests.post(
                url=f"{self.url}/uapi/overseas-stock/v1/trading/order-resv-ccnl",
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {access_token}",
                    "appkey": Global.env.KIS_APP_KEY,
                    "appsecret": Global.env.KIS_SECRET_KEY,
                    "tr_id": trade,
                },
                data=input.model_dump_json(),
            )

            return response.json()
        except Exception as e:
            print(e)
            raise e

    async def get_overseas_stock_order_resv_list(
        self,
        input: TradeDto.GetOverseasStockOrderResvListInput,
    ):
        """
        해외 주식 주문 예약 조회. 실전 투자인 경우에만 사용가능하다.
        """

        trade = TRADE_ID["usa"]["order_resv_list"]

        access_token = await self.get_access_token(input.user_id)

        try:
            response = requests.get(
                url=f"{self.url}/uapi/overseas-stock/v1/trading/order-resv-list",
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {access_token}",
                    "appkey": Global.env.KIS_APP_KEY,
                    "appsecret": Global.env.KIS_SECRET_KEY,
                    "tr_id": trade,
                },
                params=input.model_dump(),
            )

            return response.json()
        except Exception as e:
            print(e)
            raise e

    # def get_overseas_balance(
    #     self,
    #     access_token: str,
    #     order_data: TradeDto.GetOverseasBalanceInput,
    # ):
    #     """
    #     해외 주식 잔고 조회
    #     """
