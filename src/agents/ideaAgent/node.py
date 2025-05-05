from langchain_openai import ChatOpenAI
from src.agents.ideaAgent.state import IdeaState
from src.config import Global
from src.utils.baseNode import BaseNode
from langchain_core.prompts import ChatPromptTemplate
import json

class IdeaNode(BaseNode):
    def __init__(self, llm: ChatOpenAI | None = None):
        
        self.llm = (
            llm if llm else ChatOpenAI(
                model="gpt-4o-mini",
                api_key=Global.env.OPENAI_API_KEY,
            )
        )
        
        self.system_prompt = "\n".join([
            "당신은 시장 가설을 체계적으로 생성하는 전문가입니다.",
            "입력된 여러 종목(symbol) 각각에 대해 총 3개의 가설을 생성해야 합니다.",
            "물어본 종목에 대해서만 대답해주세요.",
            "종목은 팔란티어, TSMC, NVIDIA, IBM에 대한 것만 주세요.",
            "각 종목별 종목명은 다음과 같습니다: 팔란티어-PLTR, TSMC-TSM, NVIDIA-NVDA, IBM-IBM",
            "반드시 다음과 같은 JSON 포맷을 따르세요:",
            '{\n'
            '  "SYMBOL1": [\n'
            '    {\n'
            '      "hypothesis": "SYMBOL1에 대한 가설 1",\n'
            '      "confidence": 0.00\n'
            '    },\n'
            '    {\n'
            '      "hypothesis": "SYMBOL1에 대한 가설 2",\n'
            '      "confidence": 0.00\n'
            '    },\n'
            '    {\n'
            '      "hypothesis": "SYMBOL1에 대한 가설 3",\n'
            '      "confidence": 0.00\n'
            '    }\n'
            '  ],\n'
            '  "SYMBOL2": [\n'
            '    {\n'
            '      "hypothesis": "SYMBOL2에 대한 가설 1",\n'
            '      "confidence": 0.00\n'
            '    },\n'
            '    {\n'
            '      "hypothesis": "SYMBOL2에 대한 가설 2",\n'
            '      "confidence": 0.00\n'
            '    },\n'
            '    {\n'
            '      "hypothesis": "SYMBOL2에 대한 가설 3",\n'
            '      "confidence": 0.00\n'
            '    }\n'
            '  ]\n'
            '}',
            "",
            "추가적인 설명 없이 JSON만 반환해야 합니다.",
            "CoT(Chain of Thought) 사고 방식을 내부적으로 사용하되, 출력은 반드시 위 JSON 포맷만 출력하세요."
        ])
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{messages}")
        ])

    async def invoke(self, state: IdeaState) -> IdeaState:
        prompt = [{"role": "system", "content": self.system_prompt}]
        
        if isinstance(state["messages"], list):
            for m in state["messages"]:
                if isinstance(m, str):
                    prompt.append({"role": "user", "content": m})
                elif isinstance(m, tuple) and len(m) == 2:
                    role, content = m
                    prompt.append({"role": role, "content": content})
        else:
            prompt.append({"role": "user", "content": state["messages"]})

        messages = await self.llm.ainvoke(prompt)

        try:
            hypotheses = json.loads(messages.content)
            status = "success"
        except json.JSONDecodeError:
            hypotheses = {}
            status = "failed"

        return {
            **state,             # 기존 state 유지
            "hypotheses": hypotheses,
            "status": status,
        }