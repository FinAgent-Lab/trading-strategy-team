from typing import Optional
from pydantic import BaseModel, Field


class TradeNestedDto(BaseModel):
    class GetOverseasStockDailyPriceOutput1(BaseModel):
        rsym: str = Field(
            ...,
            description="""rsym is the stock code. D + market code 3 digits + stock code. ex) DNASAAPL : D + NAS(Nasdaq) + APPL(Apple)""",
        )  # 실시간조회종목코드. D + 시장구분 3자리 + 종목코드. ex) DNASAAPL : D + NAS 나스탁 + APPL 애플
        zdiv: str = Field(
            ...,
            min_length=1,
            max_length=1,
            description="""zdiv is the number of decimal places.""",
        )  # 소수점자리수
        nrec: str = Field(
            ..., description="""nrec is the previous day's closing price."""
        )  # 전일종가

    class GetOverseasStockDailyPriceOutput2(BaseModel):
        xymd: str = Field(
            ...,
            min_length=8,
            max_length=8,
            description="""xymd is the query date YYYYMMDD""",
        )  # 조회일자 YYYYMMDD
        clos: str = Field(
            ...,
            description="""clos is the closing price of the day.""",
        )  # 해당 일자의 종가
        sign: str = Field(
            ...,
            min_length=1,
            max_length=1,
            description="""sign is the symbol of the comparison. 1: up, 2: up, 3: up, 4: down, 5: down""",
        )  # 대비기호. 1: 상한, 2: 상승, 3: 보합, 4: 하락, 5: 하한
        diff: str = Field(
            ...,
            description="""diff is the difference between the closing price of the day and the previous day's closing price.""",
        )  # 대비. 해당 일자의 종가와 해당 전일 종가의 차이 (해당일 종가 - 해당 전일 종가)
        rate: str = Field(
            ...,
            description="""rate is the rate of change. (previous day's closing price / current day's closing price) * 100""",
        )  # 등락율. 해당 전일 대비 / 해당일 종가 * 100
        open: str = Field(
            ...,
            description="""open is the opening price of the day.""",
        )  # 시가. 해당일 최초 거래가격
        high: str = Field(
            ...,
            description="""high is the highest price of the day.""",
        )  # 고가. 해당일 가장 높은 거래가격
        low: str = Field(
            ...,
            description="""low is the lowest price of the day.""",
        )  # 저가. 해당일 가장 낮은 거래가격
        tvol: str = Field(
            ...,
            description="""tvol is the trading volume of the day.""",
        )  # 거래량. 해당일 거래량
        tamt: str = Field(
            ...,
            description="""tamt is the trading amount of the day.""",
        )  # 거래대금. 해당일 거래대금
        pbid: str = Field(
            ...,
            description="""pbid is the last trading price of the day.""",
        )  # 매수호가잔량. 마지막 체결이 발생한 시점의 매수호가 거래량. 해당 일자 거래량이 0인 경우 값이 수신되지 않음.
        pask: str = Field(
            ...,
            description="""pask is the last selling price of the day.""",
        )  # 매도호가. 마지막 체결이 발생한 시점의 매도호가. 해당 일자 거래량이 0인 경우 값이 수신되지 않음.
        vask: str = Field(
            ...,
            description="""vask is the last selling price of the day.""",
        )  # 매도호가잔량 해당 일자 거래량이 0인 경우 값이 수신되지 않음.

    class OrderOverseasStockOutput(BaseModel):
        KRX_FWDG_ORD_ORGNO: str = Field(
            ...,
            description="""KRX_FWDG_ORD_ORGNO is the KRX forward order organization number.""",
            max_length=5,
        )  # 한국거래소 전송 주문조직 번호.
        ODNO: str = Field(
            ...,
            description="""ODNO is the order number.""",
            max_length=10,
        )  # 주문번호.
        ORD_TMD: str = Field(
            ...,
            description="""ORD_TMD is the order time(HHMMSS).""",
            max_length=6,
        )  # 주문시간(HHMMSS).

    class BookOverseasStockOrderOutput(BaseModel):
        ODNO: str = Field(
            ...,
            max_length=10,
            description="""ODNO is the order number.""",
        )  # 한국거래소 전송 주문 조직 번호. tr_id가 TTTT3016U(미국 예약 매도 주문)/TTTT3014U(미국 예약 매수 주문)인 경우만 출력.


class TradeDto:
    class GetOverseasStockDailyPriceInput(BaseModel):
        user_id: str

        AUTH: str = Field(
            default="",
            description="Information of user authorization. AUTH is always an empty string",
        )  # 사용자권한정보. (""로 설정)
        EXCD: str = Field(
            default="NAS",
            description="""EXCD should always be "NAS", where "NAS" stands for Nasdaq.""",
        )  # 거래소코드. 나스닥 NAS
        SYMB: str = Field(
            default="TSLA",
            description="""SYMB refers to the stock code. For example, Tesla is TSLA.""",
        )  # 중목코드 ex) TSLA
        GUBN: str = Field(
            default="0",
            description="""GUBN stands for days if "0", weeks if "1", and months if "2".""",
        )  # 일/주/월 구분. 0: 일, 1: 주, 2: 월
        BYMD: str = Field(
            default="",
            description="""BYMD refers to the date of inquiry. For an empty string, it refers to today.""",
        )  # 조회기준일자 YYYYMMDD(공란시 오늘 날짜로 설정)
        MODP: str = Field(
            default="1",
            description="""MODP refers to whether or not the revised stock is reflected. 0 means the revised stock is not reflected, and 1 means the revised stock is reflected.""",
        )  # 수정주가반영여부 0: 수정주가 미반영, 1: 수정주가 반영

    class GetOverseasStockDailyPriceOutput(BaseModel):
        rt_cd: str = Field(
            ...,
            min_length=1,
            max_length=1,
            description="""rt_cd is '0' for success and other values for failure.""",
        )  # 성공 실패 여부. 0: 성공. 0 이외의 값 : 실패
        msg_cd: str = Field(
            ...,
            description="""msg_cd is the response code.""",
        )  # 응답 코드.
        msg1: str = Field(
            ...,
            description="""msg1 is the response message.""",
        )  # 응답메시지
        output1: Optional[TradeNestedDto.GetOverseasStockDailyPriceOutput1] = Field(
            ...,
        )
        output2: Optional[TradeNestedDto.GetOverseasStockDailyPriceOutput2] = Field(
            ...,
        )

    class OrderOverseasStockInput(BaseModel):
        user_id: str = Field(
            ...,
            description="""user_id is the user's id.""",
        )
        is_buy: bool = Field(
            ...,
            description="""is_buy is the order type. True: buy, False: sell""",
        )
        # CANO: str = Field(
        #     ...,
        #     min_length=8,
        #     max_length=8,
        #     description="""CANO is the combined account number. The first 8 digits of the account number.""",
        # )  # 종합계좌번호. 계좌번호 앞 8자리
        ACNT_PRDT_CD: str = Field(
            default="01",
            min_length=2,
            max_length=2,
            description="""ACNT_PRDT_CD is the account product code. The last 2 digits of the account number. 01: domestic, overseas stocks / 03: domestic futures / 08: overseas futures""",
        )  # 계좌상품코드. 계좌번호 뒤 2자리. 01: 국내, 해외주식 / 03: 국내선물 / 08: 해외선물
        OVRS_EXCG_CD: Optional[str] = Field(
            default="NASD",
            description="""OVRS_EXCG_CD is the overseas exchange code. NASD: Nasdaq / NYSE: New York Stock Exchange / AMEX: American Stock Exchange""",
        )  # 해외거래소 코드
        PDNO: str = Field(
            ...,
            max_length=12,
            description="""PDNO is the product number (stock code).""",
        )  # 상품번호(종목코드)
        ORD_QTY: str = Field(
            ...,
            description="""ORD_QTY is the order quantity.""",
        )  # 주문수량
        OVRS_ORD_UNPR: str = Field(
            default="0",
            description="""OVRS_ORD_UNPR is the overseas order unit price (1 share price). Please check the minimum order quantity and order unit for each overseas exchange. If the order is market price, please set 0.""",
        )  # 해외주문단가 (1주당 가격. 해외거래소 별 최소 주문수량 및 주문단위 확인 필요). 시장가의 경우 0으로 설정
        ORD_SVR_DVSN_CD: str = Field(
            default="0",
            description="""This field is always 0.""",
        )  # 주문서버구분코드 ("0" 으로 설정)
        ORD_DVSN: Optional[str] = Field(
            ...,
            min_length=2,
            max_length=2,
            description="""ORD_DVSN is the order division.
            ### [Header tr_id TTTT1002U(US Buy Order)]
            00 : Limit Price
            32 : LOO(Limit On Open)
            34 : LOC(Limit On Close)
            * For mock investment VTTT1002U(US Buy Order), only 00:Limit Price is available

            ### [Header tr_id TTTT1006U(US Sell Order)]
            00 : Limit Price
            31 : MOO(Market On Open)
            32 : LOO(Limit On Open)
            33 : MOC(Market On Close)
            34 : LOC(Limit On Close)
            * For mock investment VTTT1006U(US Sell Order), only 00:Limit Price is available

            ### [Header tr_id TTTS1001U(Hong Kong Sell Order)]
            00 : Limit Price
            50 : Odd Lot Limit Price
            * For mock investment VTTS1001U(Hong Kong Sell Order), only 00:Limit Price is available

            ### [Other tr_id]
            Remove
            """,
        )  # 주문구분
        """
        [Header tr_id TTTT1002U(미국 매수 주문)]
        00 : 지정가
        32 : LOO(장개시지정가)
        34 : LOC(장마감지정가)
        * 모의투자 VTTT1002U(미국 매수 주문)로는 00:지정가만 가능

        [Header tr_id TTTT1006U(미국 매도 주문)]
        00 : 지정가
        31 : MOO(장개시시장가)
        32 : LOO(장개시지정가)
        33 : MOC(장마감시장가)
        34 : LOC(장마감지정가)
        * 모의투자 VTTT1006U(미국 매도 주문)로는 00:지정가만 가능

        [Header tr_id TTTS1001U(홍콩 매도 주문)]
        00 : 지정가
        50 : 단주지정가
        * 모의투자 VTTS1001U(홍콩 매도 주문)로는 00:지정가만 가능

        [그외 tr_id]
        제거
        """

    class OrderOverseasStockOutput(BaseModel):
        rt_cd: str = Field(
            ...,
            min_length=1,
            max_length=1,
            description="""rt_cd is '0' for success and other values for failure.""",
        )  # 성공 실패 여부. 0: 성공. 0 이외의 값 : 실패
        msg_cd: str = Field(
            ...,
            description="""msg_cd is the response code.""",
        )  # 응답 코드.
        msg1: str = Field(
            ...,
            description="""msg1 is the response message.""",
        )  # 응답메시지
        output: TradeNestedDto.OrderOverseasStockOutput = Field(
            ...,
        )

    class BookOverseasStockOrderInput(BaseModel):
        user_id: str = Field(
            ...,
            description="""user_id is the user's id.""",
        )
        is_buy: bool = Field(
            ...,
            description="""is_buy is the order type. True: buy, False: sell""",
        )

        # CANO: str = Field(
        #     ...,
        #     min_length=8,
        #     max_length=8,
        #     description="""CANO is the combined account number. The first 8 digits of the account number.""",
        # )  # 종합계좌번호. 계좌번호 앞 8자리
        ACNT_PRDT_CD: str = Field(
            ...,
            min_length=2,
            max_length=2,
            description="""ACNT_PRDT_CD is the account product code. The last 2 digits of the account number. 01: domestic, overseas stocks / 03: domestic futures / 08: overseas futures""",
        )  # 계좌상품코드. 계좌번호 뒤 2자리. 01: 국내, 해외주식 / 03: 국내선물 / 08: 해외선물
        # RVSE_CNCL_DVSN_CD: str = Field(
        #     ...,
        #     min_length=2,
        #     max_length=2,
        #     description="""RVSE_CNCL_DVSN_CD is the correction cancellation code. 00: buy/sell order, 02: cancel order""",
        # )  # 정정취소구분 코드. tr_id가 TTTS3013U(중국/홍콩/일본/베트남 예약주문)인 경우만 사용. 00: 매도/매수 주문, 02: 취소
        PDNO: str = Field(
            ...,
            max_length=12,
            description="""PDNO is the product number (stock code).""",
        )  # 상품번호(종목코드)
        OVRS_EXCG_CD: str = Field(
            ...,
            max_length=4,
            description="""OVRS_EXCG_CD is the overseas exchange code. NASD: Nasdaq / NYSE: New York Stock Exchange / AMEX: American Stock Exchange""",
        )  # 해외거래소 코드
        FT_ORD_QTY: str = Field(
            ..., description="""FT_ORD_QTY is the foreign stock order quantity."""
        )  # FT주문수량
        FT_ORD_UNPR3: str = Field(
            ..., description="""FT_ORD_UNPR3 is the foreign stock order unit price."""
        )  # FT주문단가
        # ORD_DVSN: str  # tr_id가 TTTT3016U(미국 예약 매도 주문)인 경우만 사용. 00: 지정가, 31: MOO(장개시시장가)

    class BookOverseasStockOrderOutput(BaseModel):
        user_id: str = Field(
            ...,
            description="""user_id is the user's id.""",
        )
        is_buy: bool = Field(
            ...,
            description="""is_buy is the order type. True: buy, False: sell""",
        )
        rt_cd: str = Field(
            ...,
            min_length=1,
            max_length=1,
            description="""rt_cd is '0' for success and other values for failure.""",
        )  # 성공 실패 여부. 0: 성공. 0 이외의 값 : 실패
        msg_cd: str = Field(
            ..., description="""msg_cd is the response code."""
        )  # 응답 코드.
        msg1: str = Field(
            ..., description="""msg1 is the response message."""
        )  # 응답메시지
        output: TradeNestedDto.BookOverseasStockOrderOutput = Field(
            ...,
        )

    class CancelOverseasStockOrderInput(BaseModel):
        user_id: str = Field(
            ...,
            description="""user_id is the user's id.""",
        )
        # CANO: str = Field(
        #     ..., min_length=8, max_length=8
        # )  # 종합계좌번호. 계좌번호 앞 8자리
        ACNT_PRDT_CD: str = Field(
            ..., min_length=2, max_length=2
        )  # 계좌상품코드. 계좌번호 뒤 2자리. 01: 국내, 해외주식 / 03: 국내선물 / 08: 해외선물
        RSYN_ORD_RCIT_DT: str = Field(
            ..., min_length=8, max_length=8
        )  # 예약주문접수일자 YYYYMMDD
        OVRS_RSVN_ODNO: str = Field(
            ..., min_length=10, max_length=10
        )  # 해외예약주문번호

    class GetOverseasStockOrderResvListInput(BaseModel):
        user_id: str = Field(
            ...,
            description="""user_id is the user's id.""",
        )
        # CANO: str = Field(
        #     ..., min_length=8, max_length=8
        # )  # 종합계좌번호. 계좌번호 앞 8자리
        ACNT_PRDT_CD: str = Field(
            ..., min_length=2, max_length=2
        )  # 계좌상품코드. 계좌번호 뒤 2자리. 01: 국내, 해외주식 / 03: 국내선물 / 08: 해외선물
        INQR_STRT_DT: str = Field(
            ..., min_length=8, max_length=8
        )  # 조회시작일자 YYYYMMDD
        INQR_END_DT: str = Field(
            ..., min_length=8, max_length=8
        )  # 조회종료일자 YYYYMMDD
        INQR_DVSN_CD: str = Field(
            ..., min_length=2, max_length=2
        )  # 조회구분코드. 00: 전체, 01: 일반해외주식, 02: 미니스탁
        OVRS_EXCG_CD: str = Field(
            ..., max_length=4
        )  # 해외거래소 코드. NASD: 나스닥, NYSE: 뉴욕, AMEX: 아멕스
        CTX_AREA_FK200: str  # 연속조회검색 조건 200. 최초 조회시 공란. 다음 페이지 조회부터 이전 조회의 Output.CTX_AREA_FK200 값을 사용하면 된다.
        CTX_AREA_NK200: str  # 연속조회키200. 최초 조회시 공란. 다음 페이지 조회부터 이전 조회의 Output.CTX_AREA_NK200 값을 사용하면 된다.


# {
#   "CANO": "50125282",
#   "ACNT_PRDT_CD": "82",
#   "OVRS_EXCG_CD": "NASD",
#   "PDNO": "stringstring",
#   "ORD_QTY": "string",
#   "OVRS_ORD_UNPR": "string",
#   "ORD_SVR_DVSN_CD": "string",
#   "ORD_DVSN": "st"
# }
