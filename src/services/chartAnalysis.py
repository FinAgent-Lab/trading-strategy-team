from src.agents.chartAnalysisAgent.graph import chart_analysis_graph


class ChartAnalysisService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # 초기화 코드 (한 번만 호출됨)
        if not hasattr(self, "_initialized"):  # 이미 초기화된 경우는 다시 초기화하지 않음
            self._initialized = True
            self.graph = chart_analysis_graph

    def analyze_stock(self, symbol: str, exchange: str = "NAS"):
        """
        주식 차트 분석을 수행합니다.
        
        Args:
            symbol: 주식 심볼 (예: NVDA, AAPL)
            exchange: 거래소 코드 (예: NAS, NYS)
            
        Returns:
            분석 결과 메시지
        """
        initial_state = {
            "symbol": symbol,
            "exchange": exchange,
            "df": None,
            "column_description": None,
            "chart_analysis": None,
            "future_prediction": None,
            "messages": []
        }
        
        final_state = self.graph.invoke(initial_state)
        return final_state["messages"][-1][1]  # 마지막 메시지 내용 반환
