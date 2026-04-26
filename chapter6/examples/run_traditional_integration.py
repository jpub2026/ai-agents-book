"""
코드 6-1·6-2(`traditional_integration.py`)에서 정의한 TraditionalIntegration
클래스를 간단히 시연하는 데모 스크립트.

책 본문에는 포함되지 않은 보조 실행 스크립트이며, 예제 코드 자체는 변경하지 않음.

실행 전 필요한 환경 변수:
    OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY

필수 패키지:
    pip install openai anthropic google-generativeai

세 개의 키가 모두 준비되어 있지 않다면 각 서비스는 Error 문자열로
응답하며 스크립트 자체는 문제 없이 종료된다.
"""
import os

from traditional_integration import TraditionalIntegration


def main() -> None:
    integ = TraditionalIntegration()

    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    google_key = os.environ.get("GOOGLE_API_KEY")

    if openai_key:
        integ.connect_openai(openai_key)
    if anthropic_key:
        integ.connect_claude(anthropic_key)
    if google_key:
        integ.connect_gemini(google_key)

    prompt = "AI 에이전트란 무엇인지 한 문장으로 설명해 줘."
    results = integ.query_all(prompt)

    print("=== 전통적 통합 방식의 결과 ===")
    for service, answer in results.items():
        print(f"\n[{service}]\n{answer}")


if __name__ == "__main__":
    main()
