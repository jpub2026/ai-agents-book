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
