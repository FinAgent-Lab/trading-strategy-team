from src.agents.practiceAgent.graph import graph


class PracticeService:
    _instance = None

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
            self.graph = graph

    def chat_practice_agent(self, message: str):
        return self.graph.invoke({"messages": [("user", message)]})
