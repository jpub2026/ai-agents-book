from typing import Dict
from dataclasses import dataclass

# langdetect는 선택적 의존성
try:
    from langdetect import detect
except ImportError:
    def detect(text):
        return 'en'

@dataclass
class LanguageConfig:
    """언어 설정을 담는 데이터 클래스"""
    max_response_length: int = 2000
    ko_style: str = "공손하고 친절한 말투"
    en_style: str = "professional and helpful"
    ja_style: str = "丁寧で親切な口調"

class LanguageRouter:
    """언어를 감지하고 적절한 템플릿으로 라우팅하는 관리자입니다."""
    
    def __init__(self, config: LanguageConfig):
        self.config = config
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, str]:
        """언어별 프롬프트 템플릿을 로드합니다."""
        return {
            "ko": """다음 질문에 한국어로 답하세요.
                    스타일 규칙: {style}
                    질문: {query}
                    출력 형식: 최대 3개 불릿 포인트와 1줄 결론""",
                                
                                "en": """Answer in English following these guidelines.
                    Style: {style}
                    Question: {query}
                    Format: Up to 3 bullet points with a one-line conclusion""",
                                
                                "ja": """日本語で回答してください。
                    スタイル規則: {style}
                    質問: {query}
                    出力形式: 箇条書き最大3点と結論1行"""
        }
    
    def detect_language(self, text: str) -> str:
        """입력 텍스트의 언어를 자동으로 감지합니다."""
        try:
            detected = detect(text)
            if detected in ['ko', 'en', 'ja']:
                return detected
            elif detected.startswith('ja'):
                return 'ja'
            else:
                return 'en'
        except Exception as e:
            print(f"언어 감지 실패: {e}")
            return 'en'
