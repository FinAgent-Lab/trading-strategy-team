from langchain_core.prompts import ChatPromptTemplate
from src.agents.factorAgent.prompt import LogicPrompt, CodePrompt
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import initialize_agent, AgentType
import yfinance as yf
import math
import pandas as pd


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
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", LogicPrompt["system"]),
                ("human", LogicPrompt["human"].format(hypothesis=state["hypothesis"])),
            ]
        )

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

        prompt_template = ChatPromptTemplate.from_messages(
            [("system", CodePrompt["system"]), ("human", CodePrompt["human"])]
        )

        agent = initialize_agent(
            [python_tool],
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
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
        모든 알파 값의 합이 1이 되도록 정규화

        Args:
            state: 현재 상태 (alpha 포함)

        Returns:
            최종 알파 값 딕셔너리 (합이 1이 되도록 정규화)
        """
        alpha = state["alpha"]
        final_alpha = {}

        # 각 종목별 알파 값 계산
        for ticker, alpha_signals in alpha.items():
            alpha_values = [float(signal) for signal in alpha_signals]
            final_alpha[ticker] = sum(alpha_values) / len(alpha_values)

        # 모든 알파 값의 합 계산
        total_alpha = sum(final_alpha.values())

        # 알파 값 정규화 (합이 1이 되도록)
        if total_alpha != 0:  # 0으로 나누기 방지
            for ticker in final_alpha:
                final_alpha[ticker] = final_alpha[ticker] / total_alpha
        else:
            # 모든 알파 값이 0인 경우 균등 가중치 부여
            num_tickers = len(final_alpha)
            for ticker in final_alpha:
                final_alpha[ticker] = 1.0 / num_tickers

        return {"final_alpha": final_alpha}

    def rebalance_value(self, state):
        """
        포트폴리오 금액기준 리벨런싱
        """
        target_ratio = state["final_alpha"]
        # current_portfolio = state["current_portfolio"]
        current_portfolio = {
            ticker: 100 for ticker in target_ratio.keys()
        }  # 임시로 100씩 넣어둠

        total = sum(current_portfolio.values())
        out = {}
        for ticker, ratio in target_ratio.items():
            target_val = total * ratio
            out[ticker] = target_val - current_portfolio.get(ticker, 0)

        for ticker in current_portfolio.keys() - target_ratio.keys():
            out[ticker] = -current_portfolio[ticker]

        return {"rebalance_value": out}

    def rebalance_shares(self, state):
        """
        포트폴리오 주수 기준 리벨런싱
        """
        rebalance_value = state["rebalance_value"]
        prices = self.fetch_prices(rebalance_value.keys())

        shares = {}
        for ticker, cash in rebalance_value.items():
            if ticker not in prices:
                continue
            raw = cash / prices[ticker]
            adj = math.floor(raw)
            shares[ticker] = int(adj)

        return {"rebalance_shares": shares}

    def fetch_prices(self, tickers):
        """
        주식 종목의 최근 종가 가져오기
        """
        closes = yf.download(
            tickers, period="1d", interval="1d", group_by="ticker", progress=False
        )
        if len(tickers) == 1:
            t = tickers[0]
            return {t: float(closes["Close"].iloc[-1])}  # type: ignore
        return {t: float(closes[t]["Close"].iloc[-1]) for t in tickers}  # type: ignore
