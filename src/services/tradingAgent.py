from src.agents.tradeAgent.graph import TradeGraph
from src.agents.tradingAgent.tradingAgent import TradingAgent


class TradingAgentService:
    _instance = None
    graph: TradeGraph

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
            self.graph = TradeGraph()

    def chat_trading_agent(self, input: str):
        agent = TradingAgent()
        return agent.get_response(input)

    async def chat_trade_agent(self, room_id: str, user_id: str, input: str):
        return await self.graph.invoke(room_id, user_id, input)
