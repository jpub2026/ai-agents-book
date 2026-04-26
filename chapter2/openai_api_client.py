"""
OpenAI API를 사용하는 클라이언트 예제
- 실행 전 `pip install openai python-dotenv` 가 필요합니다.
- OPENAI_API_KEY 환경 변수 또는 .env 파일이 있어야 동작합니다.
"""
import os
import sys


class OpenAIClient:
    """OpenAI API를 사용하는 클라이언트"""

    def __init__(self):
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError(
                "openai 패키지가 필요합니다. `pip install openai` 로 설치해 주세요."
            ) from e

        # 환경변수에서 API 키 로드 (python-dotenv 가 있으면 .env 도 함께 로드)
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except ImportError:
            # python-dotenv 가 없어도 환경변수에 키가 있으면 동작합니다.
            pass

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "OPENAI_API_KEY 환경 변수가 설정되지 않았습니다."
            )

        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        """OpenAI 모델로 텍스트 생성"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"API 호출 오류: {e}"


if __name__ == "__main__":
    try:
        openai_client = OpenAIClient()
    except (ImportError, EnvironmentError) as e:
        print(f"[안내] {e}")
        sys.exit(0)

    response = openai_client.generate("파이썬의 장점을 간단히 설명해주세요.")
    print("응답:", response)
