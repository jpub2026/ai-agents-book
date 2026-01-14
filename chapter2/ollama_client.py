import requests
import json

class OllamaClient:
    """
    Ollama를 사용하여 로컬 LLM을 실행하는 클라이언트
    """
    
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, model: str, prompt: str) -> str:
        """
        로컬 모델로 텍스트 생성
        """
        # API 호출
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        
        # 응답 처리
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"오류: {response.status_code}"
    
    def list_models(self) -> list:
        """
        설치된 모델 목록 확인
        """
        response = requests.get(f"{self.base_url}/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [m['name'] for m in models]
        return []

# 사용 예제
ollama = OllamaClient()

# 모델 목록 확인
print("설치된 모델:", ollama.list_models())

# 텍스트 생성
response = ollama.generate(
    model="llama3.2",
    prompt="파이썬의 장점을 간단히 설명해주세요."
)
print("응답:", response)
