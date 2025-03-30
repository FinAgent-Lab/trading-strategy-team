import pandas as pd
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from src.config import Global
from src.agents.chartAnalysisAgent.state import ChartAnalysisState
import requests


# OpenAI API 설정
llm = ChatOpenAI(model="gpt-4o-mini", api_key=Global.env.OPENAI_API_KEY)

# 한국투자증권 API 설정
KIS_API_URL = "https://openapi.koreainvestment.com:9443/uapi/overseas-price/v1/quotations/dailyprice"


# 주가 데이터 가져오기 함수
def fetch_stock_data(symbol="NVDA", exchange="NAS", days=30):
    from src.services.kis import KisService
    
    headers = {
        "authorization": f"Bearer {KisService.ACCESS_TOKEN}",
        "appkey": KisService.APP_KEY,
        "appsecret": KisService.APP_SECRET,
        "tr_id": "HHDFS76240000",
        "content-type": "application/json; charset=utf-8"
    }
    
    params = {
        "AUTH": "",
        "EXCD": exchange,  # 거래소 코드 (예: NAS - 나스닥)
        "SYMB": symbol,     # 종목 코드 (예: NVDA - NVIDIA)
        "GUBN": "0",        # 0: 일봉 데이터
        "BYMD": "",         # 공란: 오늘 날짜 기준 조회
        "MODP": "0"         # 수정 주가 반영 여부
    }
    
    response = requests.get(KIS_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["rt_cd"] == "0":
            return pd.DataFrame(data["output2"])  # output2에 날짜별 시세 정보 포함
        else:
            raise Exception(f"API 응답 오류: {data['msg1']}")
    else:
        raise Exception(f"API 요청 실패: {response.status_code}")


# 주가 데이터 가져오기 (LangGraph Node)
def get_stock_data(state: ChartAnalysisState) -> ChartAnalysisState:
    print(f"� {state['symbol']} 주가 데이터 가져오는 중...")
    df = fetch_stock_data(state['symbol'], state['exchange'])
    df["date"] = pd.to_datetime(df["xymd"], format="%Y%m%d")
    df = df.rename(columns={"clos": "close", "open": "open", "high": "high", "low": "low", "tvol": "volume"})
    df = df[["date", "close", "open", "high", "low", "volume"]]
    
    state['df'] = df
    return state


# 컬럼 설명 생성 (GPT-4o-mini 사용)
def describe_columns(state: ChartAnalysisState) -> ChartAnalysisState:
    prompt = f"""
    다음은 {state['symbol']}의 주가 데이터 컬럼 목록입니다:
    {list(state['df'].columns)}

    각 컬럼의 의미를 설명하고, 주가 분석에서 어떻게 활용할 수 있는지 정리해 주세요.
    """
    response = llm.invoke([SystemMessage(content="You are a financial analyst."), HumanMessage(content=prompt)])
    state['column_description'] = response.content
    return state


# 차트 분석 수행 (GPT-4o-mini 사용)
def analyze_chart(state: ChartAnalysisState) -> ChartAnalysisState:
    prompt = f"""
    다음은 {state['symbol']}의 최근 30일간 주가 데이터입니다:
    {state['df'].to_string(index=False)}

    이 데이터를 바탕으로 주가 분석을 수행하세요:
    - 최근 주가 추세 (상승/하락/횡보)
    - 변동성이 큰 구간 식별
    - 기술적 분석 요소 (이동평균선, 지지선, 저항선)
    """
    response = llm.invoke([SystemMessage(content="You are a stock market analyst."), HumanMessage(content=prompt)])
    state['chart_analysis'] = response.content
    return state


# 향후 주가 예측 수행 (GPT-4o-mini 사용)
def predict_future(state: ChartAnalysisState) -> ChartAnalysisState:
    prompt = f"""
    최근 30일간 {state['symbol']}의 주가 데이터입니다:
    {state['df'].to_string(index=False)}

    이 데이터를 기반으로 향후 주가 변동을 예측하세요.
    - 상승/하락 가능성
    - 주요 지지선/저항선
    - 투자자들에게 조언할 사항
    """
    response = llm.invoke([SystemMessage(content="You are a stock market forecaster."), HumanMessage(content=prompt)])
    state['future_prediction'] = response.content
    return state


# 차트 시각화 함수
def plot_chart(state: ChartAnalysisState) -> ChartAnalysisState:
    plt.figure(figsize=(10, 5))
    plt.plot(state['df']["date"], state['df']["close"], marker="o", linestyle="-", label="종가 (Close)")
    plt.xticks(rotation=45)
    plt.title(f"{state['symbol']} 주가 차트 (30일)")
    plt.xlabel("날짜")
    plt.ylabel("가격 ($)")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"static/charts/{state['symbol']}_chart.png")
    plt.close()
    
    # 메시지에 차트 이미지 경로 추가
    state['messages'].append(("system", f"차트 이미지가 생성되었습니다: /static/charts/{state['symbol']}_chart.png"))
    return state


# 결과 요약 노드
def summarize_results(state: ChartAnalysisState) -> ChartAnalysisState:
    summary = f"""
    ## {state['symbol']} 주가 분석 결과
    
    ### 1. 컬럼 설명
    {state['column_description']}
    
    ### 2. 차트 분석
    {state['chart_analysis']}
    
    ### 3. 향후 주가 예측
    {state['future_prediction']}
    """
    
    state['messages'].append(("system", summary))
    return state