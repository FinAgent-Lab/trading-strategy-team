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

            # self.url = "https://openapi.koreainvestment.com:9443"  # 실전 투자 url

            self.url = "https://openapivts.koreainvestment.com:29443"  # 모의 투자 url

    def get_access_token(self) -> str:
        """
        KIS 액세스 토큰 발급
        """

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
        input: TradeDto.GetOverseasStockDailyPriceInput,
    ) -> TradeDto.GetOverseasStockDailyPriceOutput:
        """
        해외 주식 기간별 시세
        """

        try:
            response = requests.get(
                url=f"{self.url}/uapi/overseas-price/v1/quotations/dailyprice",
                headers={
                    "Authorization": f"Bearer {input.access_token}",
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

    def order_overseas_stock(
        self,
        input: TradeDto.OrderOverseasStockInput,
        is_buy: bool,
    ) -> dict:
        """
        해외 주식 주문
        """

        trade = TRADE_ID["usa"]["buy"] if is_buy else TRADE_ID["usa"]["sell"]

        try:
            response = requests.post(
                url=f"{self.url}/uapi/overseas-stock/v1/trading/order",
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {input.access_token}",
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

    def book_overseas_stock_order(
        self,
        input: TradeDto.BookOverseasStockOrderInput,
        is_buy: bool,
    ):
        """
        해외 주식 주문 예약
        """

        trade = TRADE_ID["usa"]["buy"] if is_buy else TRADE_ID["usa"]["sell"]

        try:
            response = requests.post(
                url=f"{self.url}/uapi/overseas-stock/v1/trading/order-resv",
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {input.access_token}",
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

    def cancel_overseas_stock_order(
        self,
        input: TradeDto.CancelOverseasStockOrderInput,
    ):
        """
        해외 주식 주문 취소
        """

        trade = TRADE_ID["usa"]["book_cancel"]

        try:
            response = requests.post(
                url=f"{self.url}/uapi/overseas-stock/v1/trading/order-resv-ccnl",
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {input.access_token}",
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

    def get_overseas_stock_order_resv_list(
        self,
        input: TradeDto.GetOverseasStockOrderResvListInput,
    ):
        """
        해외 주식 주문 예약 조회. 실전 투자인 경우에만 사용가능하다.
        """

        trade = TRADE_ID["usa"]["order_resv_list"]

        try:
            response = requests.get(
                url=f"{self.url}/uapi/overseas-stock/v1/trading/order-resv-list",
                headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {input.access_token}",
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
