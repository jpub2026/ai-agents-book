import os
import requests
from typing import Optional, Dict, Any
import json

class LLM:
    """
    이 책의 모든 예제에서 사용할 통합 LLM 인터페이스
    자동으로 최적의 제공자를 선택합니다
    """
    
    def __init__(self, provider: str = "auto", model: str = None):
        """
        LLM 인터페이스 초기화
        provider: "auto", "ollama", "openai", "mock" 중 선택
        model: 사용할 모델명 (None이면 기본값 사용)
        """
        # 제공자 자동 감지 또는 수동 설정
        if provider == "auto":
            self.provider = self._detect_provider()
        else:
            self.provider = provider

        # 모델 설정
        self.model = model or self._get_default_model()

        # 클라이언트 초기화
        self._initialize_client()
        
        print(f" LLM 초기화 완료: {self.provider} ({self.model})")
    
    def _detect_provider(self) -> str:
        """
        사용 가능한 LLM 제공자를 자동으로 감지
        우선순위: Ollama  OpenAI  Mock
        """
        # Ollama 확인
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=1)
            if response.status_code == 200:
                print(" Ollama 감지됨")
                return "ollama"
        except:
            pass
        
        # OpenAI API 키 확인
        if os.getenv("OPENAI_API_KEY"):
            print(" OpenAI API 키 감지됨")
            return "openai"
        
        # 둘 다 없으면 Mock 모드
        print("Ollama와 OpenAI가 없어 테스트 모드로 실행합니다")
        print(" - Ollama 설치: https://ollama.ai")
        print(" - OpenAI 설정: export OPENAI_API_KEY='your-key'")
        return "mock"
    
    def _get_default_model(self) -> str:
        """각 제공자의 기본 모델 반환"""
        defaults = {
            "ollama": "llama3.2",
            "openai": "gpt-3.5-turbo",
            "mock": "mock-model"
        }
        return defaults.get(self.provider, "unknown")
    
    def _initialize_client(self):
        """선택된 제공자에 따라 클라이언트 초기화"""
        if self.provider == "ollama":
            self.base_url = "http://localhost:11434"
        elif self.provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
        # Mock는 별도 초기화 불필요
    
    def generate(self, prompt: str, temperature: float = 0.7, 
                max_tokens: int = 500) -> str:
        """
        모든 장에서 동일하게 사용할 텍스트 생성 메서드
        """
        if self.provider == "ollama":
            return self._ollama_generate(prompt, temperature, max_tokens)
        elif self.provider == "openai":
            return self._openai_generate(prompt, temperature, max_tokens)
        else:
            return self._mock_generate(prompt)
    
    def _ollama_generate(self, prompt: str, temperature: float, 
                        max_tokens: int) -> str:
        """Ollama를 사용한 텍스트 생성"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    },
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"Ollama 오류: {response.status_code}"
        except Exception as e:
            return f"Ollama 오류: {str(e)}"
        
    def _openai_generate(self, prompt: str, temperature: float, 
                        max_tokens: int) -> str:
        """OpenAI API를 사용한 텍스트 생성"""
        try:
            from openai import OpenAI # ImportError 처리 위해 내부로 이동
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except ImportError:
            return "OpenAI 라이브러리가 설치되지 않았습니다. pip install openai"
        except Exception as e:
            return f"OpenAI 오류: {str(e)}"
    
    def _mock_generate(self, prompt: str) -> str:
        """테스트용 Mock 응답 생성"""
        # ReAct 에이전트 형식 감지
        if "Thought:" in prompt and "Action:" in prompt and "Final Answer:" in prompt:
            # 이미 Observation이 있으면 Final Answer 생성
            if "Observation:" in prompt and ("14일" in prompt or "3-5 영업일" in prompt or "7일" in prompt):
                return """Thought: FAQ 도구에서 필요한 정보를 얻었으므로 최종 답변을 준비합니다.
Final Answer: 검색 결과를 바탕으로 답변드립니다. 자세한 내용은 위의 관측 결과를 참고해주세요."""
            # FAQ 관련 질문 처리
            elif "환불" in prompt:
                return """Thought: 사용자가 환불 정책에 대해 질문하고 있습니다. FAQ 도구를 사용해서 환불 정보를 찾아보겠습니다.
Action: faq_search
Action Input: 환불"""
            elif "배송" in prompt:
                return """Thought: 사용자가 배송에 대해 질문하고 있습니다. FAQ 도구를 사용해서 배송 정보를 찾아보겠습니다.
Action: faq_search
Action Input: 배송"""
            elif "교환" in prompt:
                return """Thought: 사용자가 교환에 대해 질문하고 있습니다. FAQ 도구를 사용해서 교환 정보를 찾아보겠습니다.
Action: faq_search
Action Input: 교환"""
            else:
                return """Thought: 질문을 이해하고 FAQ 도구를 사용해보겠습니다.
Action: faq_search
Action Input: 정보"""

        # 프롬프트에 따라 적절한 테스트 응답 생성
        responses = {
            "계획": "1. 첫 번째 단계\n2. 두 번째 단계\n3. 세 번째 단계",
            "코드": "def example():\n    return 'Hello, World!'",
            "설명": "이것은 테스트 응답입니다. 실제 LLM 응답을 시뮬레이션합니다.",
            "번역": "This is a translation example.",
            "요약": "주요 내용: 테스트 시뮬레이션"
        }

        # 프롬프트에서 키워드 찾기
        for keyword, response in responses.items():
            if keyword in prompt:
                return response

        # 기본 응답
        return f"[Mock 응답] '{prompt[:50]}...'에 대한 시뮬레이션 응답입니다."

# 사용 예제
if __name__ == "__main__":
    # 자동 감지 모드
    llm = LLM()
    
    # 간단한 테스트
    response = llm.generate("파이썬의 장점을 간단히 설명해주세요.")
    print(f"\n응답: {response}")


