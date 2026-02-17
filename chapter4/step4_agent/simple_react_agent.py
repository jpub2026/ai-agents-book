# 간단한 ReAct 에이전트-구성 요소 초기화
"""
가장 간단한 ReAct 에이전트
목표: 도구를 사용해서 질문에 답하기
"""

import sys
from pathlib import Path
from langchain.agents import AgentExecutor, create_react_agent
# LangChain 1.0 환경에서는 다음과 같이 임포트합니다:
# from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

# 이전 단계의 모듈들을 불러옵니다.
sys.path.append(str(Path(__file__).parent.parent))
from step2_real_llm.cached_llm_bridge import CachedLLMBridge
from step3_tools.hybrid_faq_tool import HybridFAQTool


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

    def _create_prompt(self) -> PromptTemplate:
        """ReAct 프롬프트 템플릿 생성"""  # ❶

        template = """당신은 친절한 FAQ 도우미입니다.

사용 가능한 도구:
{tools}

도구 이름: {tool_names}

사용자 질문: {input}

다음 형식을 정확히 따라서 단계별로 생각하고 답변하세요:

Thought: 사용자의 질문을 이해하고, 어떤 정보를 찾아야 할지 생각합니다.
Action: 사용할 도구의 이름을 정확히 적습니다.
Action Input: 도구에 전달할 검색어나 질문을 적습니다.
Observation: (도구의 실행 결과가 자동으로 여기에 나타납니다)

필요하다면 위 과정을 반복할 수 있습니다.

Thought: 이제 충분한 정보를 얻었으므로 최종 답변을 준비합니다.
Final Answer: 사용자에게 친절하고 명확한 답변을 제공합니다.

시작하세요!

{agent_scratchpad}"""  # ❷

        return PromptTemplate(
            input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
            template=template
        )

    def ask(self, question: str) -> str:
        """사용자 질문에 답변합니다"""
        try:
            print(f"\n{'='*60}")
            print(f"User Question: {question}")
            print(f"{'='*60}\n")

            # 에이전트 실행
            result = self.executor.invoke({"input": question})
            return result["output"]

        except Exception as e:
            return f"죄송합니다. 오류가 발생했습니다: {e}"


if __name__ == "__main__":
    # 에이전트 생성 및 테스트
    agent = SimpleReActAgent()

    # 테스트 질문
    test_questions = [
        "환불 정책이 어떻게 되나요?",
        "배송은 얼마나 걸려요?",
    ]

    for question in test_questions:
        print(f"\n질문: {question}")
        print("-" * 50)
        answer = agent.ask(question)
        print(f"답변: {answer}")
