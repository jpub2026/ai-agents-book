from abc import ABC, abstractmethod
import re

class LanguageProcessor(ABC):
    """모든 언어 프로세서가 구현해야 하는 인터페이스입니다."""
    
    @abstractmethod
    def preprocess(self, text: str) -> str:
        """입력 텍스트를 정규화하고 전처리합니다."""
        pass
    
    @abstractmethod
    def postprocess(self, text: str) -> str:
        """생성된 응답을 언어 규칙에 맞게 후처리합니다."""
        pass 
