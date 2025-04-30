import json
import pandas as pd
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.schema import SystemMessage, HumanMessage
from src.config import Global
from src.agents.chartAnalysisAgent.state import ChartAnalysisState
from src.utils.baseNode import BaseNode
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import ToolCall
import requests
from src.services.kis import KisService
from src.agents.chartAnalysisAgent.prompt import ChartAnalysisPrompt
from typing import List
from pydantic import BaseModel, Field
from src.dtos.kis.tradeDto import TradeDto
from src.agents.tools.chartTool import get_overseas_stock_daily_price
import pandas_ta as ta


# Tool의 입력 스키마 정의
class GetStockDataInput(BaseModel):
    AUTH: str = Field(default="", description="사용자권한정보")
    EXCD: str = Field(description="거래소코드 (예: NAS)")
    SYMB: str = Field(description="종목코드 (예: NVDA)")
    GUBN: str = Field(default="0", description="일/주/월 구분 (0: 일)")
    BYMD: str = Field(default="", description="조회기준일자")
    MODP: str = Field(default="0", description="수정주가반영여부")
    access_token: str = Field(default="", description="접근 토큰")


class ChartAnalysisAgent:
    llm: ChatOpenAI
    llm_with_tools: ChatOpenAI
    system_prompt: str
    prompt_template: ChatPromptTemplate
    tools: List[Tool]

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=Global.env.OPENAI_API_KEY)
        self.system_prompt = ChartAnalysisPrompt.system_prompt
        self.prompt_template = ChatPromptTemplate.from_messages(
            [("system", self.system_prompt), ("human", "{input}")]
        )
        self.kis_service = KisService()

        # Tools
        self.tools = [
            Tool(
                name="get_overseas_stock_daily_price",
                description=get_overseas_stock_daily_price.__doc__,
                func=get_overseas_stock_daily_price,
                args_schema=TradeDto.GetOverseasStockDailyPriceInput,
            )
        ]

        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def get_stock_data(self, input: GetStockDataInput):
        """해외 주식 일별 시세를 조회합니다."""
        # KisService에서 토큰 가져오기
        access_token = self.kis_service.get_access_token()
        input_dict = input.model_dump()
        input_dict["access_token"] = access_token
        
        # KisService를 통해 데이터 가져오기
        response = self.kis_service.get_overseas_stock_daily_price(input_dict)
        return response

    def analyze_chart(self, symbol: str, exchange: str) -> str:
        try:
            print(f"[ChartAnalysis] 차트 분석 시작 - 심볼: {symbol}, 거래소: {exchange}")
            
            # KisService에서 access_token 가져오기
            print("[ChartAnalysis] access_token 요청 중...")
            access_token = self.kis_service.get_access_token()
            print(f"[ChartAnalysis] access_token 획득 완료: {access_token[:20]}...")  # 토큰의 앞부분만 출력
            
            # Tool 입력 생성
            print("[ChartAnalysis] 주가 데이터 요청 준비 중...")
            tool_input = {
                "input": {
                    "access_token": access_token,
                    "AUTH": "",
                    "EXCD": exchange,
                    "SYMB": symbol,
                    "GUBN": "0",
                    "BYMD": "",
                    "MODP": "0"
                }
            }
            print("[ChartAnalysis] 입력 데이터 구성 완료")
            
            # Tool 직접 호출
            print("[ChartAnalysis] KIS API 호출 중...")
            result = get_overseas_stock_daily_price(tool_input)
            print("[ChartAnalysis] KIS API 응답 수신")
            print(f"[ChartAnalysis] 응답 데이터: {result}")
            
            if result.get('rt_cd') != '0':
                raise Exception(f"API 오류: {result.get('msg1', '알 수 없는 오류')}")
                
            output2_list = result.get('output2', [])
            if output2_list and len(output2_list) > 0:
                data_list = []
                for output2 in output2_list:
                    date_str = output2['xymd']
                    formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
                    data_list.append({
                        'date': formatted_date,
                        'close': float(output2['clos']),
                        'open': float(output2['open']),
                        'high': float(output2['high']),
                        'low': float(output2['low']),
                        'volume': int(output2['tvol'])
                    })

                data = pd.DataFrame(data_list)
                data["date"] = pd.to_datetime(data["date"])
                data.sort_values("date", inplace=True)

                # ✅ SMA 계산 추가
                data["SMA_5"] = ta.sma(data["close"], length=5)
                data["SMA_20"] = ta.sma(data["close"], length=20)
                data["SMA_60"] = ta.sma(data["close"], length=60)
                # ✅ RSI 계산 추가 (14일 기준)
                data["RSI_14"] = ta.rsi(data["close"], length=14)

                print(f"[ChartAnalysis] 데이터프레임 생성 완료 (총 {len(data)} 행):")
                print(f"[ChartAnalysis] 최근 5일 데이터:\n{data.tail()}")

                # ✅ SMA 포함한 프롬프트
                analysis_prompt = f"""
                {symbol} 주식의 최근 {len(data)}일간의 거래 및 이동평균선(SMA) 데이터입니다:

                최근 종가: ${data['close'].iloc[-1]:,.2f}
                최고가: ${data['high'].max():,.2f}
                최저가: ${data['low'].min():,.2f}
                평균 거래량: {int(data['volume'].mean()):,}
                RSI(14일): {data['RSI_14'].iloc[-1]:.2f}

                최근 10일 데이터 (SMA & RSI 포함):
                {data[['date', 'close', 'SMA_5', 'SMA_20', 'SMA_60', 'RSI_14']].tail(10).to_string(index=False)}

                다음 내용을 중심으로 기술적 분석을 수행해주세요:
                1. 가격 추세와 이동평균선 분석 (골든/데드크로스 포함)
                2. RSI 수치를 기반으로 한 과매수/과매도 판단
                3. 주요 지지/저항 구간
                4. 향후 주가 움직임 예측 및 투자 조언
                """

                print("[ChartAnalysis] 프롬프트 생성 완료")
                print("[ChartAnalysis] AI 분석 수행 중...")
                analysis_result = self.llm.invoke(analysis_prompt)
                print("[ChartAnalysis] AI 분석 완료")

                return analysis_result
            else:
                print("[ChartAnalysis] 오류: output2 데이터가 없습니다")
                return "주가 데이터를 가져오는데 실패했습니다."
            
        except Exception as e:
            error_msg = f"[ChartAnalysis] 오류 발생: {str(e)}"
            print(error_msg)
            return error_msg

    def execute_tool_call(self, tool_call: ToolCall) -> str:
        tool_name = tool_call["name"]
        tool_input = tool_call["args"]
        tool = next((t for t in self.tools if t.name == tool_name), None)
        if tool:
            # DTO 객체로 변환하여 전달
            input_dto = TradeDto.GetOverseasStockDailyPriceInput(**tool_input)
            return tool.func(input_dto)
        return "Tool not found"

class ChartAnalysisNode(BaseNode):
    def __init__(self, llm: ChatOpenAI | None = None):
        self.llm = (
            lambda: (
                llm
                if llm
                else ChatOpenAI(
                    model="gpt-4o-mini",
                    api_key=Global.env.OPENAI_API_KEY,
                )
            )
        )()
        
        self.system_prompt = "\n".join([
            "You are a financial analyst specialized in chart analysis.",
            "Analyze the stock data and provide insights about:",
            "1. Column descriptions and their significance",
            "2. Recent price trends and patterns",
            "3. Future predictions based on technical analysis",
            "Use the provided tools to fetch and analyze stock data.",
        ])
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{messages}")
        ])

        # KIS API 설정
        self.KIS_API_URL = "https://openapi.koreainvestment.com:9443/uapi/overseas-price/v1/quotations/dailyprice"
        
        # Tools 설정
        self.tools = [
            Tool(
                name="fetch_stock_data",
                description="Fetch stock price data from KIS API",
                func=self.fetch_stock_data,
            ),
            Tool(
                name="analyze_chart",
                description="Analyze stock chart patterns and trends",
                func=self.analyze_chart,
            ),
            Tool(
                name="predict_future",
                description="Predict future stock price movements",
                func=self.predict_future,
            )
        ]

        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def fetch_stock_data(self, state: ChartAnalysisState):
        headers = {
            "authorization": f"Bearer {state['access_token']}",
            "appkey": Global.env.KIS_APP_KEY,
            "appsecret": Global.env.KIS_APP_SECRET,
            "tr_id": "HHDFS76240000",
            "content-type": "application/json; charset=utf-8"
        }
        
        params = {
            "AUTH": "",
            "EXCD": state['exchange'],
            "SYMB": state['symbol'],
            "GUBN": "0",
            "BYMD": "",
            "MODP": "0"
        }
        
        response = requests.get(self.KIS_API_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data["rt_cd"] == "0":
                df = pd.DataFrame(data["output2"])
                df["date"] = pd.to_datetime(df["xymd"], format="%Y%m%d")
                df = df.rename(columns={
                    "clos": "close",
                    "open": "open",
                    "high": "high",
                    "low": "low",
                    "tvol": "volume"
                })
                state['df'] = df[["date", "close", "open", "high", "low", "volume"]]
                return state
            else:
                raise Exception(f"API 응답 오류: {data['msg1']}")
        else:
            raise Exception(f"API 요청 실패: {response.status_code}")

    def analyze_chart(self, state: ChartAnalysisState):
        prompt = f"""
        다음은 {state['symbol']}의 최근 주가 데이터입니다:
        {state['df'].to_string(index=False)}

        이 데이터를 바탕으로 주가 분석을 수행하세요:
        - 최근 주가 추세 (상승/하락/횡보)
        - 변동성이 큰 구간 식별
        - 기술적 분석 요소 (이동평균선, 지지선, 저항선)
        """
        response = self.llm.invoke([
            SystemMessage(content="You are a stock market analyst."),
            HumanMessage(content=prompt)
        ])
        state['chart_analysis'] = response.content
        return state

    def predict_future(self, state: ChartAnalysisState):
        prompt = f"""
        최근 {state['symbol']}의 주가 데이터입니다:
        {state['df'].to_string(index=False)}

        이 데이터를 기반으로 향후 주가 변동을 예측하세요.
        - 상승/하락 가능성
        - 주요 지지선/저항선
        - 투자자들에게 조언할 사항
        """
        response = self.llm.invoke([
            SystemMessage(content="You are a stock market forecaster."),
            HumanMessage(content=prompt)
        ])
        state['future_prediction'] = response.content
        return state

    def invoke(self, state: ChartAnalysisState):
        try:
            # 데이터 가져오기
            state = self.fetch_stock_data(state)
            
            # 차트 분석
            state = self.analyze_chart(state)
            
            # 미래 예측
            state = self.predict_future(state)
            
            # 결과 생성
            result = {
                "symbol": state['symbol'],
                "exchange": state['exchange'],
                "chart_analysis": state['chart_analysis'],
                "future_prediction": state['future_prediction']
            }
            
            return {
                "messages": [json.dumps(result)],
                "processed": ["content"]
            }
            
        except Exception as e:
            error_message = f"Error in ChartAnalysisNode: {str(e)}"
            return {
                "messages": [json.dumps({"error": error_message})],
                "processed": ["error"]
            }