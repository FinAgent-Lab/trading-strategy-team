from typing import Annotated
from fastapi import APIRouter, Depends, Path

from src.dtos.kis.tradeDto import TradeDto
from src.services.kis import KisService

kis_router = router = APIRouter(prefix="/kis")


@router.get("/access-token/{user_id}")
async def get_access_token(
    user_id: Annotated[str, Path(..., description="User ID")],
    kis_service: KisService = Depends(lambda: KisService()),
):
    return await kis_service.get_access_token(user_id)


@router.post(
    "/foreign-stock/daily-price",
    tags=["해외 주식"],
    summary="해외 주식 기간별 시세",
    description="""
        **Request Body**<br>
        AUTH  # 사용자권한정보. (""로 설정)<br>
        EXCD  # 거래소코드. 나스닥 NAS<br>
        SYMB  # 중목코드 ex) TSLA<br>
        GUBN  # 일/주/월 구분. 0: 일, 1: 주, 2: 월<br>
        BYMD  # 조회기준일자 YYYYMMDD(공란시 오늘 날짜로 설정)<br>
        MODP  # 수정주가반영여부 0: 수정주가 미반영, 1: 수정주가 반영<br>
        --------------------------------------------------------------------------------------------<br>
        **Response Body**<br>
        rt_cd  # 성공 실패 여부. 0: 성공. 0 이외의 값 : 실패<br>
        msg_cd  # 응답 코드.<br>
        msg1  # 응답메시지<br>
        ### output1<br>
        rsym  # 실시간조회종목코드. D + 시장구분 3자리 + 종목코드. ex) DNASAAPL : D + NAS 나스탁 + APPL 애플<br>
        zdiv  # 소수점자리수<br>
        nrec  # 전일종가<br>
        ### output2<br>
        xymd  # 조회일자 YYYYMMDD<br>
        clos  # 종가<br>
        sign  # 대비기호. 1: 상한, 2: 상승, 3: 보합, 4: 하락, 5: 하한<br>
        diff  # 대비. 해당 일자의 종가와 해당 전일 종가의 차이 (해당일 종가 - 해당 전일 종가)<br>
        rate  # 등락율. 해당 전일 대비 / 해당일 종가 * 100<br>
        open  # 시가. 해당일 최초 거래가격<br>
        high  # 고가. 해당일 가장 높은 거래가격<br>
        low  # 저가. 해당일 가장 낮은 거래가격<br>
        tvol  # 거래량. 해당일 거래량<br>
        tamt  # 거래대금. 해당일 거래대금<br>
        pbid  # 매수호가. 마지막 체결이 발생한 시점의 매수호가. 해당 일자 거래량이 0인 경우 값이 수신되지 않음.<br>
        vbid  # 매수호가잔량. 마지막 체결이 발생한 시점의 매수호가 거래량. 해당 일자 거래량이 0인 경우 값이 수신되지 않음.<br>
        pask  # 매도호가. 마지막 체결이 발생한 시점의 매도호가. 해당 일자 거래량이 0인 경우 값이 수신되지 않음.<br>
        vask  # 매도호가잔량 해당 일자 거래량이 0인 경우 값이 수신되지 않음.<br>
    """,
)
async def get_overseas_stock_daily_price(
    access_token: str,
    input: TradeDto.GetOverseasStockDailyPriceInput,
    kis_service: KisService = Depends(lambda: KisService()),
):
    return kis_service.get_overseas_stock_daily_price(
        {**input, "access_token": access_token}
    )


@router.post(
    "/foreign-stock/order",
    tags=["해외 주식"],
    summary="해외 주식 주문",
    description="""
        **Request Body**<br>
        CANO  # 종합계좌번호. 계좌번호 앞 8자리<br>
        ACNT_PRDT_CD  # 계좌상품코드. 계좌번호 뒤 2자리<br>
        OVRS_EXCG_CD  # 해외거래소 코드<br>
        PDNO  # 상품번호(종목코드)<br>
        ORD_QTY  # 주문수량<br>
        OVRS_ORD_UNPR  # 해외주문단가 (1주당 가격. 해외거래소 별 최소 주문수량 및 주문단위 확인 필요)<br>
        ORD_SVR_DVSN_CD  # 주문서버구분코드 ("0" 으로 설정)<br>
        ORD_DVSN  # 주문구분<br>
    """,
)
async def order_foreign_stock(
    access_token: str,
    input: TradeDto.OrderOverseasStockInput,
    isBuy: bool,
    kis_service: KisService = Depends(lambda: KisService()),
):
    return kis_service.order_overseas_stock(access_token, input, isBuy)


@router.post(
    "/foreign-stock/book",
    tags=["해외 주식"],
    summary="해외 주식 주문 예약",
    description="""
        **Request Body**<br>
        CANO  # 종합계좌번호. 계좌번호 앞 8자리<br>
        ACNT_PRDT_CD  # 계좌상품코드. 계좌번호 뒤 2자리<br>
        RVSE_CNCL_DVSN_CD  # 00으로 두면 될듯.<br>
        OVRS_EXCG_CD  # 해외거래소 코드<br>
        PDNO  # 상품번호(종목코드)<br>
        FT_ORD_QTY  # FT주문수량<br>
        FT_ORD_UNPR3  # FT주문단가<br>
    """,
)
async def book_foreign_stock_order(
    access_token: str,
    input: TradeDto.BookOverseasStockOrderInput,
    isBuy: bool,
    kis_service: KisService = Depends(lambda: KisService()),
):
    return kis_service.book_overseas_stock_order(access_token, input, isBuy)
