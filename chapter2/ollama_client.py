"""
Ollama 로컬 LLM을 사용하는 클라이언트 예제
- 이 스크립트는 Ollama 서버가 로컬에서 실행 중이어야 동작합니다.
- Ollama 설치: https://ollama.com
- 모델 내려받기 예: `ollama pull llama3.2`
"""
import requests


class OllamaClient:
    """Ollama를 사용하여 로컬 LLM을 실행하는 클라이언트"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def generate(self, model: str, prompt: str) -> str:
        """로컬 모델로 텍스트 생성"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=60,
            )
        except requests.exceptions.RequestException as e:
            return f"Ollama 서버에 연결할 수 없습니다: {e}"

        if response.status_code == 200:
            return response.json()["response"]
        return f"오류: {response.status_code}"

    def list_models(self) -> list:
        """설치된 모델 목록 확인"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
        except requests.exceptions.RequestException:
            return []

        if response.status_code == 200:
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        return []


if __name__ == "__main__":
    ollama = OllamaClient()

    # 모델 목록 확인
    models = ollama.list_models()
    print("설치된 모델:", models if models else "(Ollama 서버가 실행 중이 아닙니다)")

    # 텍스트 생성 (서버가 실행 중이고 모델이 설치되어 있어야 합니다)
    response = ollama.generate(
        model="llama3.2",
        prompt="파이썬의 장점을 간단히 설명해주세요.",
    )
    print("응답:", response)
