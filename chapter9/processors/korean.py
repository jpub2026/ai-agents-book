import re
from abc import ABC, abstractmethod

class LanguageProcessor(ABC):
    """언어 처리기의 기본 클래스"""
    @abstractmethod
    def preprocess(self, text: str) -> str:
        pass

    @abstractmethod
    def postprocess(self, text: str) -> str:
        pass

class KoreanProcessor(LanguageProcessor):
    """한국어 텍스트의 전처리와 후처리를 담당합니다."""
    
    def preprocess(self, text: str) -> str:
        """한국어 입력을 정규화합니다."""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[?？]+', '?', text)
        return text.strip()
    
    def postprocess(self, text: str) -> str:
        """한국어 응답의 문체와 형식을 보정합니다."""
        if not text.endswith(('다.', '요.', '까?')):
            text += '습니다.'
        
        text = re.sub(r'^[-*]\s*', '• ', text, flags=re.MULTILINE)
        text = re.sub(r'님께서는', '님은', text)
        
        return text
