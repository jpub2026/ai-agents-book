"""
세 번째 버전: 캐싱 기능 추가
목표: 반복 질문에 대한 효율성 향상
"""

import sys
import logging
from datetime import datetime, timedelta
import hashlib
from pathlib import Path
from typing import Any, List, Optional

from langchain_core.language_models import BaseLLM
from langchain_core.outputs import Generation, LLMResult

# 부모 디렉터리의 모듈을 불러오기 위한 경로 추가
sys.path.append(str(Path(__file__).parent.parent.parent))
from chapter2.llm_interface import LLM

logger = logging.getLogger(__name__)


class CachedLLMBridge(BaseLLM):
    """캐싱 기능이 있는 LLM 브리지"""

    # Pydantic 필드 정의
    llm: Any = None
    _cache: dict = {}
    cache_ttl: Any = None
    cache_hits: int = 0
    cache_misses: int = 0

    def __init__(self, provider: str = "auto", cache_ttl: int = 3600):
        """
        초기화
        cache_ttl: 캐시 유효 시간 (초 단위, 기본 1시간)
        """
        super().__init__()
        self.llm = LLM(provider=provider)
        self._cache = {}
        self.cache_ttl = timedelta(seconds=cache_ttl)
        self.cache_hits = 0
        self.cache_misses = 0

    def _generate_cache_key(self, prompt: str, **kwargs) -> str:
        """캐시 키 생성"""
        # 프롬프트와 파라미터를 조합하여 유니크한 키 생성
        key_source = f"{prompt}:{kwargs.get('temperature', 0.7)}:{kwargs.get('max_tokens', 500)}"
        return hashlib.md5(key_source.encode()).hexdigest()

    def _is_cache_valid(self, cache_entry: dict) -> bool:
        """캐시 항목이 유효한지 확인"""
        if not cache_entry:
            return False

        age = datetime.now() - cache_entry['timestamp']
        return age < self.cache_ttl

    @property
    def _llm_type(self) -> str:
        return "cached-bridge"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> str:
        """캐싱이 적용된 LLM 호출"""

        # 캐시 키 생성
        cache_key = self._generate_cache_key(prompt, **kwargs)

        # 캐시 확인
        if cache_key in self._cache:
            cache_entry = self._cache[cache_key]
            if self._is_cache_valid(cache_entry):
                self.cache_hits += 1
                hit_rate = self.get_cache_hit_rate()
                logger.info(f"Cache hit! (hit rate: {hit_rate:.1%})")
                return cache_entry['response']

        # 캐시 미스 - 실제 LLM 호출
        self.cache_misses += 1
        response = self.llm.generate(prompt, **kwargs)

        # stop 단어 처리
        if stop:
            for stop_word in stop:
                if stop_word in response:
                    response = response.split(stop_word)[0]

        # 캐시에 저장
        self._cache[cache_key] = {
            'response': response,
            'timestamp': datetime.now()
        }

        return response

    def get_cache_hit_rate(self) -> float:
        """캐시 히트율 계산"""
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0

    async def _acall(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        return self._call(prompt, stop, **kwargs)

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        **kwargs: Any
    ) -> LLMResult:
        """BaseLLM의 추상 메서드 구현"""
        generations = []
        for prompt in prompts:
            text = self._call(prompt, stop, **kwargs)
            generations.append([Generation(text=text)])
        return LLMResult(generations=generations)
