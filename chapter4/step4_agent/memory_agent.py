"""
메모리가 있는 ReAct 에이전트
목표: 이전 대화를 기억하고 맥락을 이해하기
"""
import sys

# 부모 디렉토리의 모듈을 import하기 위한 경로 추가
sys.path.append('..')
sys.path.append('../step2_real_llm')
sys.path.append('../step3_tools')

from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

from cached_llm_bridge import CachedLLMBridge
from simple_faq_tool import SimpleFAQTool as ImprovedFAQTool


class MemoryReActAgent:
    """대화를 기억하는 에이전트"""
    
    def __init__(self, memory_type: str = "buffer"):
        """
        에이전트 초기화
        memory_type: "buffer" 또는 "summary"
        """
        print(f"Initializing agent with {memory_type} memory...")
        
        # 기본 컴포넌트들
        self.llm = CachedLLMBridge(provider="mock")
        self.tools = [ImprovedFAQTool()]
        
        # 메모리 타입 선택
        if memory_type == "buffer":
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=False,  # 문자열 형식 사용
                output_key="output"
            )
            print("Using Buffer Memory (stores complete history)")
        elif memory_type == "summary":
            self.memory = ConversationSummaryMemory(
                llm=self.llm,
                memory_key="chat_history",
                return_messages=False
            )
            print("Using Summary Memory (stores condensed history)")
        else:
            raise ValueError(f"Unknown memory type: {memory_type}")
        
        # 메모리를 포함한 프롬프트 생성
        self.prompt = self._create_prompt_with_memory()
        
        # 에이전트와 실행자 생성
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,  # 메모리 연결
            verbose=False,  # 깔끔한 출력
            max_iterations=3,
            handle_parsing_errors=True
        )
        
        print("Memory-enabled agent ready!\n")
    
    def _create_prompt_with_memory(self) -> PromptTemplate:
        """메모리를 고려한 프롬프트 템플릿"""
        
        template = """당신은 친절한 FAQ 도우미입니다.

                이전 대화 내용:
                {chat_history}

                사용 가능한 도구:
                {tools}

                도구 이름: {tool_names}

                현재 사용자 질문: {input}

                중요: 이전 대화를 참고하여 맥락을 이해하세요.
                - "그것", "그거", "아까 말한" 같은 대명사가 나오면 이전 대화를 확인하세요.
                - 사용자가 추가 질문을 하면 이전 답변을 기반으로 대답하세요.

                답변 형식:
                Thought: (이전 대화를 고려하여 생각)
                Action: (필요한 도구)
                Action Input: (검색어)
                Observation: (관찰)
                Final Answer: (맥락을 고려한 최종 답변)

                {agent_scratchpad}"""
        
        return PromptTemplate(
            input_variables=["chat_history", "tools", "tool_names", "input", "agent_scratchpad"],
            template=template
        )
    
    def chat(self, message: str) -> str:
        """대화 처리"""
        try:
            result = self.executor.invoke({"input": message})
            return result["output"]
        except Exception as e:
            return f"죄송합니다. 오류가 발생했습니다: {e}"
    
    def clear_memory(self):
        """대화 기록 초기화"""
        self.memory.clear()
        print("Conversation memory cleared.")
    
    def show_memory(self):
        """현재 메모리 내용 표시"""  # ❹
        memory_vars = self.memory.load_memory_variables({})
        print("\n=== Current Memory ===")
        if 'chat_history' in memory_vars:
            print(memory_vars['chat_history'])
        else:
            print("(empty)")
        print("=" * 40 + "\n")
