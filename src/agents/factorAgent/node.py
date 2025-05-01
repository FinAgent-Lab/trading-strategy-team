from langchain_core.prompts import ChatPromptTemplate
from src.agents.factorAgent.prompt import LogicPrompt, CodePrompt
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import initialize_agent, AgentType


class FactorAgent:
    """
    금융 가설을 AST로 변환하고 알파 신호를 계산하는 에이전트 클래스
    """
    def __init__(self, llm):
        """
        FactorAgent 초기화
        
        Args:
            llm: 사용할 언어 모델
        """
        self.llm = llm

    def generate_ast(self, state):
        """
        금융 가설을 IF-THEN-ELSE 형태의 AST로 변환
        
        Args:
            state: 현재 상태 (hypothesis 포함)
            
        Returns:
            AST 딕셔너리
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", LogicPrompt["system"]),
            ("human", LogicPrompt["human"].format(hypothesis=state["hypothesis"]))
        ])

        chain = prompt | self.llm
        
        hypothesis_dict = state["hypothesis"]
        ast = {}

        for ticker, hypothesis_list in hypothesis_dict.items():
            ast[ticker] = []
            for hypothesis in hypothesis_list:
                response = chain.invoke({"hypothesis": hypothesis})
                ast[ticker].append(response.content)

        return {"ast": ast}
    
    def execute_code(self, state):
        """
        AST를 기반으로 Python 코드를 실행하여 알파 신호 계산
        
        Args:
            state: 현재 상태 (ast 포함)
            
        Returns:
            알파 신호 딕셔너리
        """
        python_tool = PythonREPLTool()

        ast = state["ast"]

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", CodePrompt["system"]),
            ("human", CodePrompt["human"])
        ])

        agent = initialize_agent(
            [python_tool],  
            self.llm,  
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

        alpha = {}
        for ticker, ast_list in ast.items():
            alpha_signal = []
            for ast_item in ast_list:
                formatted_prompt = prompt_template.format(ast=ast_item, ticker=ticker)
                response = agent.run(formatted_prompt)
                alpha_signal.append(response.content)

            alpha[ticker] = alpha_signal

        return {"alpha": alpha}

    def final_output(self, state):
        """
        개별 알파 신호들을 종합하여 최종 알파 값 계산
        
        Args:
            state: 현재 상태 (alpha 포함)
            
        Returns:
            최종 알파 값 딕셔너리
        """
        alpha = state["alpha"]
        final_alpha = {}
        
        for ticker, alpha_signals in alpha.items():
            # 문자열로 된 알파 신호들을 float으로 변환
            alpha_values = [float(signal) for signal in alpha_signals]
            # 평균값 계산
            final_alpha[ticker] = sum(alpha_values) / len(alpha_values)
            
        return {"final_alpha": final_alpha}
