from langchain_core.messages import ToolCall
from langchain_openai import ChatOpenAI
from src.agents.ideaAgent.state import IdeaState
from src.config import Global
from src.utils.baseNode import BaseNode
from langchain_core.prompts import ChatPromptTemplate
from langchain_teddynote.tools.tavily import TavilySearch
from langchain_core.tools import Tool

class IdeaNode(BaseNode):
    def __init__(self, llm: ChatOpenAI | None = None):
        self.llm = (
            llm
            if llm
            else ChatOpenAI(
                model="gpt-4o-mini",
                api_key=Global.env.OPENAI_API_KEY,
            )
        )
        self.system_prompt = "\n".join([
            "당신은 시장 가설을 체계적으로 생성하는 전문가입니다.",
            "다음의 요소들을 고려하여 가설을 생성해야 합니다:",
            "1. 지식: 기존 금융 이론과 실무자 경험",
            "2. 시장 관측: 현재 시장 상황 및 패턴 분석",
            "3. 정당화: 관측된 패턴과 경제적 메커니즘 간의 연결",
            "4. 가설의 시간적 특성: 패턴 기반의 트리거",
            "5. 구현 제약: 숫자 파라미터나 time window 등의 구체적 조건",
            "",
            "아래 JSON 포맷을 **반드시 그대로** 따르세요. **추가 설명 없이 JSON만** 출력하세요.",
            "",
            "형식 예시:",
            '{\n'
            '  "reasoning": "가설을 생성하는 근거를 여기에 작성하세요.",\n'
            '  "hypothesis": "한 문장 이내로 가설을 작성하세요.",\n'
            '  "confidence": "0.00 ~ 1.00 사이의 수치를 문자열로 입력하세요."\n'
            '}',
            "",
            "다시 말하지만, 반드시 위와 같은 JSON 포맷으로만 출력해야 합니다. 추가 문장이나 설명을 작성하지 마세요.",
            "",
            "CoT(Chain of Thought) 방식을 사용하여 내부적으로 사고한 뒤, 최종 출력은 JSON으로만 작성하세요."
        ])
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{messages}")
        ])


    def invoke(self, state: IdeaState):
        prompt = [{"role": "system", "content": self.system_prompt}] + state["messages"]
        messages = self.llm.invoke(prompt)
        
        return {
            # "charts": "차트 정보",
            "messages": [messages.content],
            "hypothesis": "[messages.content]",
            "confidence": "가설의 신뢰도 수준, 0.00~1.00"
        }
        