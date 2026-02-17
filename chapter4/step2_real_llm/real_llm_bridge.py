# 실제 LLM과 연결된 브리지-기본 구조와 초기화
"""
두 번째 버전: 실제 LLM과 연결
목표: 2장의 LLM 인터페이스를 사용하기
"""

import sys
from pathlib import Path
from langchain_core.language_models import LLM
from langchain_core.outputs import Generation, LLMResult
from typing import Any, List, Optional
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2장 코드를 불러오기
sys.path.append(str(Path(__file__).parent.parent.parent / 'chapter2'))
from llm_interface import LLM


class RealLLMBridge(LLM):
    """실제 LLM과 연결된 브리지"""

    # Pydantic 필드 선언
    llm: Any = None
    provider: str = "auto"

    def __init__(self, provider: str = "auto"):  
        """
        초기화 메서드
        provider: LLM 제공자 ("auto", "ollama", "openai", "mock")
        """
        super().__init__()

        # 2장에서 만든 LLM 인터페이스 사용  
        self.llm = LLM(provider=provider)
        self.provider = provider

        # 초기화 성공 로그
        logger.info(f"LLM Bridge initialized - Provider: {provider}")

    @property
    def _llm_type(self) -> str:
        """LLM 타입을 반환합니다"""
        return f"real-bridge-{self.provider}"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs: Any
    ) -> str:
        """실제 LLM을 호출합니다"""
        try:
            # 로그: 호출 시작
            logger.debug(f"Starting LLM call: {prompt[:50]}...")

            # 2장의 LLM 인터페이스 사용
            response = self.llm.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # 로그: 호출 완료
            logger.debug(f"LLM response received: {response[:50]}...")

            return response

        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> LLMResult:
        """BaseLLM의 필수 추상 메서드 구현"""
        generations = []
        for prompt in prompts:
            response = self._call(prompt, stop=stop, **kwargs)
            generations.append([Generation(text=response)])
        return LLMResult(generations=generations)
