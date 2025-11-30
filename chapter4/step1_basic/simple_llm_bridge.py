"""
첫 번째 버전: 정말 간단한 LLM 브리지
목표: LangChain과 우리의 LLM을 연결만 하기
"""

from langchain_core.language_models import BaseLLM
from langchain_core.outputs import Generation, LLMResult
from typing import Any, List, Optional

class SimpleLLMBridge(BaseLLM):
    """가장 간단한 형태의 LLM 브리지"""

    @property
    def _llm_type(self) -> str:
        """LLM의 이름을 정합니다"""
        return "simple-bridge"

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> LLMResult:
        """
        BaseLLM의 필수 추상 메서드
        여러 프롬프트를 처리하고 LLMResult를 반환합니다
        """
        generations = []
        for prompt in prompts:
            text = self._call(prompt, stop, **kwargs)
            generations.append([Generation(text=text)])
        return LLMResult(generations=generations)

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> str:
        """
        LLM을 호출하는 핵심 메서드
        지금은 가짜 응답을 만들어 반환합니다
        """
        # 실제 LLM 대신 간단한 규칙으로 응답 생성
        if "환불" in prompt:
            return "환불은 구매 후 14일 이내에 가능합니다."
        elif "배송" in prompt:
            return "배송은 보통 3-5일 걸립니다."
        else:
            return "죄송합니다. 그 질문에는 답변할 수 없습니다."

    async def _acall(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> str:
        """비동기 버전 (지금은 동기 버전을 그대로 호출)"""
        return self._call(prompt, stop, **kwargs)

# 테스트 코드
if __name__ == "__main__":
    # 우리가 만든 브리지를 생성합니다
    llm = SimpleLLMBridge()
    
    # 간단한 테스트
    test_cases = [
        "환불 정책이 궁금해요",
        "배송은 언제 되나요?", 
        "날씨가 어때요?"
    ]
    
    for question in test_cases:
        answer = llm._call(question)
        print(f"Q: {question}")
        print(f"A: {answer}\n")
