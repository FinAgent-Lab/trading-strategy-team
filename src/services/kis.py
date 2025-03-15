import json
import requests
from src.dtos.kis.tradeDto import TradeDto
from src.config import Global
from src.utils.constants.trId import TRADE_ID


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

            # self.url = "https://openapi.koreainvestment.com:9443" # 실전 투자 url

            self.url = "https://openapivts.koreainvestment.com:29443"  # 모의 투자 url

    def get_access_token(self) -> str:
        """
        KIS 액세스 토큰 발급
        """

        print(Global.env.KIS_APP_KEY)
        print(Global.env.KIS_SECRET_KEY)

        response = requests.post(
            url=f"{self.url}/oauth2/tokenP",
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

    def get_overseas_stock_daily_price(
        self,
        access_token: str,
        input: TradeDto.GetOverseasStockDailyPriceInputDto,
    ) -> dict:
        """
        해외 주식 기간별 시세
        """

        trade = TRADE_ID["usa"]["buy"]

        # try:
        print("-----input-----")
        print(input)
        print("-----input-----")

        response = requests.get(
            url=f"{self.url}/uapi/overseas-price/v1/quotations/dailyprice",
            headers={
                "Authorization": f"Bearer {access_token}",
                "appkey": Global.env.KIS_APP_KEY,
                "appsecret": Global.env.KIS_SECRET_KEY,
                "tr_id": trade,
            },
            params=input,
        )

        print(f"📌 요청 URL: {response.url}")
        print(f"🔹 응답 코드: {response.status_code}")
        print(f"🔹 응답 내용: {response.text}")

        return response.json()
        # except Exception as e:
        #     print(e)
        #     raise e

    def order_overseas_stock(
        self,
        access_token: str,
        order_data: TradeDto.OrderOverseasStockInputDto,
        isBuy: bool,
    ) -> dict:
        """
        해외 주식 주문
        """

        trade = TRADE_ID["usa"]["buy"] if isBuy else TRADE_ID["usa"]["sell"]

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
                data=json.dumps(order_data),
            )

            return response.json()
        except Exception as e:
            print(e)
            raise e

    def book_overseas_stock_order(
        self,
        access_token: str,
        order_data: TradeDto.BookOverseasStockOrderInputDto,
        isBuy: bool,
    ):
        """
        해외 주식 주문 예약
        """

        trade = TRADE_ID["usa"]["buy"] if isBuy else TRADE_ID["usa"]["sell"]

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
                data=json.dumps(order_data),
            )

            return response.json()
        except Exception as e:
            print(e)
            raise e
