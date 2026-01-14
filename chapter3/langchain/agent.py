from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun
import os

class LangChainAgent:
    """
    LangChain 프레임워크를 활용한 에이전트
    
    우리가 직접 구현했던 것과 같은 기능을 
    훨씬 간단하게 구현할 수 있습니다.
    """
    
    def __init__(self, openai_api_key: str = None):
        """
        LangChain 에이전트를 초기화합니다.
        
        우리가 했던 것처럼 LLM, Memory, Tools를 설정하지만,
        프레임워크가 많은 부분을 자동으로 처리해줍니다.
        """
        # API 키 설정
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # LLM 초기화 - 우리의 LLM 클래스와 비슷한 역할
        self.llm = OpenAI(temperature=0.7)
        
        # 메모리 설정 - 우리의 MemorySystem과 같은 역할
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # 도구 설정 - 우리의 ToolManager와 Tools
        self.tools = self._setup_tools()

        # 에이전트 초기화 - 우리의 Agent 클래스 전체를 대체!
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True  # 실행 과정을 출력
        )
    
    def _setup_tools(self) -> list:
        """
        에이전트가 사용할 도구들을 설정합니다.
        """
        tools = []
        
        # 웹 검색 도구 - 실제로 작동하는 도구!
        search = DuckDuckGoSearchRun()
        tools.append(
            Tool(
                name="Search",
                func=search.run,
                description="인터넷에서 최신 정보를 검색할 때 사용합니다"
            )
        )
        
        return tools
    
    def process_request(self, user_request: str) -> str:
        """
        사용자 요청을 처리합니다.
        
        우리가 4단계로 구현했던 복잡한 프로세스가
        단 한 줄로 처리됩니다!
        """
        # 이 한 줄이 우리의 전체 process_request 메서드를 대체합니다
        response = self.agent.run(user_request)
        return response
