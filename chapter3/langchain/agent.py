"""
LangChain 프레임워크로 같은 에이전트를 구성하는 예제.

- 실행 전 `pip install langchain langchain-openai langchain-community duckduckgo-search` 가 필요합니다.
- OPENAI_API_KEY 환경 변수가 없으면 예제는 안내만 출력하고 종료합니다.
"""
import os
import sys


class LangChainAgent:
    """LangChain 프레임워크를 활용한 에이전트"""

    def __init__(self, openai_api_key: str = None):
        try:
            from langchain.agents import AgentType, Tool, initialize_agent
            from langchain.memory import ConversationBufferMemory
            from langchain_openai import OpenAI
            from langchain_community.tools import DuckDuckGoSearchRun
        except ImportError as e:
            raise ImportError(
                "LangChain 관련 패키지가 필요합니다. "
                "`pip install langchain langchain-openai langchain-community duckduckgo-search` 로 설치해 주세요."
            ) from e

        # API 키 설정
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError(
                "OPENAI_API_KEY 환경 변수가 설정되지 않았습니다."
            )

        # LLM 초기화
        self.llm = OpenAI(temperature=0.7)

        # 메모리 설정
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )

        # 도구 설정
        search = DuckDuckGoSearchRun()
        self.tools = [
            Tool(
                name="Search",
                func=search.run,
                description="인터넷에서 최신 정보를 검색할 때 사용합니다.",
            )
        ]

        # 에이전트 초기화
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
        )

    def process_request(self, user_request: str) -> str:
        """사용자 요청을 처리합니다."""
        return self.agent.run(user_request)


if __name__ == "__main__":
    try:
        agent = LangChainAgent()
    except (ImportError, EnvironmentError) as e:
        print(f"[안내] {e}")
        sys.exit(0)

    print(agent.process_request("LangChain에 대해 간단히 알려줘."))
