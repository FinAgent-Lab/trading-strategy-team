from src.agents.chartAnalysisAgent.node import ChartAnalysisAgent
import logging

logger = logging.getLogger(__name__)

class ChartAnalysisService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.agent = ChartAnalysisAgent()

    def analyze_stock(self, symbol: str, exchange: str = "NAS"):
        try:
            logger.info(f"Starting analysis for {symbol} on {exchange}")
            result = self.agent.analyze_chart(symbol, exchange)
            return result
        except Exception as e:
            logger.error(f"Error in analyze_stock: {str(e)}")
            raise
