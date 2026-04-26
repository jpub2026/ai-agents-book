"""
메모리가 있는 ReAct 에이전트
목표: 이전 대화를 기억하고 맥락을 이해하기
"""
import os
import sys
from pathlib import Path

# 부모 디렉터리의 모듈을 불러오기 위해 __file__ 기준으로 경로를 추가합니다.
_CH4_DIR = Path(__file__).resolve().parent.parent
for _p in (
    _CH4_DIR,
    _CH4_DIR / "step2_real_llm",
    _CH4_DIR / "step3_tools",
):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.agents import create_react_agent, AgentExecutor
# LangChain 1.0 환경에서는 다음과 같이 임포트합니다:
# from langchain_classic.memory import ConversationBufferMemory, ConversationSummaryMemory
# from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

from cached_llm_bridge import CachedLLMBridge
from simple_faq_tool import SimpleFAQTool


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
        self.tools = [SimpleFAQTool()]
        
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


if __name__ == "__main__":
    agent = MemoryReActAgent(memory_type="buffer")

    print(agent.chat("환불 정책이 어떻게 되나요?"))
    print(agent.chat("그러면 교환은요?"))
    agent.show_memory()
