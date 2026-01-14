import tiktoken

class TokenAnalyzer:
    """
    텍스트의 토큰화를 분석하고 API 비용을 예측하는 도구
    """
    
    def __init__(self):
        # GPT 모델의 토큰화 방식
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
        # 토큰당 가격(1,000토큰 기준, USD)
        self.price_per_1k = {
            "gpt-3.5": 0.002,
            "gpt-4": 0.03
        }
    
    def analyze(self, text: str) -> dict:
        """텍스트를 분석하여 토큰 정보를 반환합니다"""
        # 토큰화
        tokens = self.encoding.encode(text)
        token_count = len(tokens)
        
        # 언어별 효율성 계산
        char_count = len(text)
        chars_per_token = char_count / token_count if token_count > 0 else 0
        
        # 예상 비용 계산
        cost_gpt35 = (token_count / 1000) * self.price_per_1k["gpt-3.5"]
        cost_gpt4 = (token_count / 1000) * self.price_per_1k["gpt-4"]
        
        return {
            "text": text[:50] + "..." if len(text) > 50 else text,
            "token_count": token_count,
            "character_count": char_count,
            "chars_per_token": round(chars_per_token, 1),
            "estimated_cost": {
                "gpt-3.5": f"${cost_gpt35:.4f}",
                "gpt-4": f"${cost_gpt4:.4f}"
            }
        }

# 다양한 언어 테스트
analyzer = TokenAnalyzer()

texts = {
    "영어": "Hello, how are you?",
    "한글": "안녕하세요, 어떻게 지내세요?",
    "코드": "def hello(): print('Hello')"
}

for lang, text in texts.items():
    result = analyzer.analyze(text)
    print(f"\n{lang}: {text}")
    print(f"  토큰 수: {result['token_count']}")
    print(f"  문자당 토큰: {result['chars_per_token']}")
