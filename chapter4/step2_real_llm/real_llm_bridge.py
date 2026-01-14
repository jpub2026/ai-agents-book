# 실제 LLM과 연결된 브리지-기본 구조와 초기화
"""
두 번째 버전: 실제 LLM과 연결
목표: 2장의 LLM 인터페이스를 사용하기
"""

import sys
from pathlib import Path
from langchain_core.language_models import BaseLLM
from typing import Any, List, Optional
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2장 코드를 불러오기
sys.path.append(str(Path(__file__).parent.parent.parent / 'chapter2'))
from llm_interface import LLM


class RealLLMBridge(BaseLLM):
    """실제 LLM과 연결된 브리지"""

    def __init__(self, provider: str = "auto"):  # ❶
        """
        초기화 메서드
        provider: LLM 제공자 ("auto", "ollama", "openai", "mock")
        """
        super().__init__()

        # 2장에서 만든 LLM 인터페이스 사용  # ❷
        self.llm = LLM(provider=provider)
        self.provider = provider

        # 초기화 성공 로그
        logger.info(f"LLM Bridge initialized - Provider: {provider}")

    @property
    def _llm_type(self) -> str:  # ❸
        """LLM 타입을 반환합니다"""
        return f"real-bridge-{self.provider}"
