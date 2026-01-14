# 간단한 ReAct 에이전트-구성 요소 초기화
"""
가장 간단한 ReAct 에이전트
목표: 도구를 사용해서 질문에 답하기
"""

import sys
from pathlib import Path
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

# 이전 단계의 모듈들을 불러온다.
sys.path.append(str(Path(__file__).parent.parent))
from step2_real_llm.cached_llm_bridge import CachedLLMBridge
from step3_tools.improved_faq_tool import ImprovedFAQTool


class SimpleReActAgent:
    """간단한 ReAct 에이전트"""

    def __init__(self):
        """에이전트를 초기화합니다"""

        print("Initializing ReAct Agent...")

        # 1. LLM 준비(캐싱 기능 포함)
        self.llm = CachedLLMBridge(provider="mock")  # ❶

        # 2. 도구 준비
        self.tools = [ImprovedFAQTool()]
        print(f"Loaded {len(self.tools)} tool(s)")

        # 3. 프롬프트 템플릿 생성
        self.prompt = self._create_prompt()

        # 4. ReAct 에이전트 생성(LangChain 0.3 방식)  # ❷
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        # 5. 실행자 생성  # ❸
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,  # 실행 과정을 출력
            max_iterations=3,  # 최대 세 번의 사고-행동 사이클
            handle_parsing_errors=True  # 파싱 오류 자동 처리
        )

        print("Agent ready!\n")
