from pydantic import BaseModel, Field


class TradeDto:
    class GetOverseasStockDailyPriceInputDto(BaseModel):
        AUTH: str = ""  # 사용자권한정보. (""로 설정)
        EXCD: str = "NAS"  # 거래소코드. 나스닥 NAS
        SYMB: str = "TSLA"  # 중목코드 ex) TSLA
        GUBN: str = "0"  # 일/주/월 구분. 0: 일, 1: 주, 2: 월
        BYMD: str = ""  # 조회기준일자 YYYYMMDD(공란시 오늘 날짜로 설정)
        MODP: str = "1"  # 수정주가반영여부 0: 수정주가 미반영, 1: 수정주가 반영

    class OrderOverseasStockInputDto(BaseModel):
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

    class BookOverseasStockOrderInputDto(BaseModel):
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
