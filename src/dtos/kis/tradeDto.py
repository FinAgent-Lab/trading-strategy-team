from typing import Optional
from pydantic import BaseModel, Field


class TradeNestedDto(BaseModel):
    class GetOverseasStockDailyPriceOutput1(BaseModel):
        rsym: str = Field(
            ...
        )  # 실시간조회종목코드. D + 시장구분 3자리 + 종목코드. ex) DNASAAPL : D + NAS 나스탁 + APPL 애플
        zdiv: str = Field(..., min_length=1, max_length=1)  # 소수점자리수
        nrec: str  # 전일종가

    class GetOverseasStockDailyPriceOutput2(BaseModel):
        xymd: str = Field(..., min_length=8, max_length=8)  # 조회일자 YYYYMMDD
        clos: str  # 종가
        sign: str = Field(
            ..., min_length=1, max_length=1
        )  # 대비기호. 1: 상한, 2: 상승, 3: 보합, 4: 하락, 5: 하한
        diff: str  # 대비. 해당 일자의 종가와 해당 전일 종가의 차이 (해당일 종가 - 해당 전일 종가)
        rate: str  # 등락율. 해당 전일 대비 / 해당일 종가 * 100
        open: str  # 시가. 해당일 최초 거래가격
        high: str  # 고가. 해당일 가장 높은 거래가격
        low: str  # 저가. 해당일 가장 낮은 거래가격
        tvol: str  # 거래량. 해당일 거래량
        tamt: str  # 거래대금. 해당일 거래대금
        pbid: str  # 매수호가. 마지막 체결이 발생한 시점의 매수호가. 해당 일자 거래량이 0인 경우 값이 수신되지 않음.
        vbid: str  # 매수호가잔량. 마지막 체결이 발생한 시점의 매수호가 거래량. 해당 일자 거래량이 0인 경우 값이 수신되지 않음.
        pask: str  # 매도호가. 마지막 체결이 발생한 시점의 매도호가. 해당 일자 거래량이 0인 경우 값이 수신되지 않음.
        vask: str  # 매도호가잔량 해당 일자 거래량이 0인 경우 값이 수신되지 않음.


class TradeDto:
    class GetOverseasStockDailyPriceInput(BaseModel):
        access_token: str
        AUTH: str = Field(default="")  # 사용자권한정보. (""로 설정)
        EXCD: str = Field(default="NAS")  # 거래소코드. 나스닥 NAS
        SYMB: str = Field(default="TSLA")  # 중목코드 ex) TSLA
        GUBN: str = Field(default="0")  # 일/주/월 구분. 0: 일, 1: 주, 2: 월
        BYMD: str = Field(default="")  # 조회기준일자 YYYYMMDD(공란시 오늘 날짜로 설정)
        MODP: str = Field(
            default="1"
        )  # 수정주가반영여부 0: 수정주가 미반영, 1: 수정주가 반영

    class GetOverseasStockDailyPriceOutput(BaseModel):
        rt_cd: str = Field(
            ..., min_length=1, max_length=1
        )  # 성공 실패 여부. 0: 성공. 0 이외의 값 : 실패
        msg_cd: str  # 응답 코드.
        msg1: str  # 응답메시지
        output1: Optional[TradeNestedDto.GetOverseasStockDailyPriceOutput1] = None
        output2: Optional[TradeNestedDto.GetOverseasStockDailyPriceOutput2] = None

    class OrderOverseasStockInput(BaseModel):
        CANO: str = Field(
            ..., min_length=8, max_length=8
        )  # 종합계좌번호. 계좌번호 앞 8자리
        ACNT_PRDT_CD: str = Field(
            ..., min_length=2, max_length=2
        )  # 계좌상품코드. 계좌번호 뒤 2자리
        OVRS_EXCG_CD: str = Field(..., min_length=4, max_length=4)  # 해외거래소 코드
        PDNO: str = Field(..., min_length=12, max_length=12)  # 상품번호(종목코드)
        ORD_QTY: str  # 주문수량
        OVRS_ORD_UNPR: str  # 해외주문단가 (1주당 가격. 해외거래소 별 최소 주문수량 및 주문단위 확인 필요)
        ORD_SVR_DVSN_CD: str  # 주문서버구분코드 ("0" 으로 설정)
        ORD_DVSN: str = Field(..., min_length=2, max_length=2)  # 주문구분

    class BookOverseasStockOrderInput(BaseModel):
        CANO: str = Field(
            ..., min_length=8, max_length=8
        )  # 종합계좌번호. 계좌번호 앞 8자리
        ACNT_PRDT_CD: str = Field(
            ..., min_length=2, max_length=2
        )  # 계좌상품코드. 계좌번호 뒤 2자리
        RVSE_CNCL_DVSN_CD: str = Field(
            ..., min_length=2, max_length=2
        )  # 00으로 두면 될듯.
        OVRS_EXCG_CD: str = Field(..., min_length=4, max_length=4)  # 해외거래소 코드
        PDNO: str = Field(..., min_length=12, max_length=12)  # 상품번호(종목코드)
        FT_ORD_QTY: str  # FT주문수량
        FT_ORD_UNPR3: str  # FT주문단가


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
