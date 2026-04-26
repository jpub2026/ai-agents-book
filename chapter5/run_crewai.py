"""
코드 5-10 ~ 5-12(`crewai_agents.py`)의 CrewAITeam을 손쉽게 실행할 수 있는
데모 스크립트.

책 본문에는 포함되지 않은 보조 실행 스크립트이며, 예제 코드 자체는 변경하지 않음.

필수 패키지:
    pip install crewai langchain-openai python-dotenv

사전 조건:
    OPENAI_API_KEY 환경 변수가 필요하다. `.env` 파일 또는 쉘 환경 변수로
    설정해 두면 `dotenv`가 자동으로 로드한다.

참고:
    책 본문에서는 `gpt-4o-mini` 모델을 사용한다고 설명하지만 저장소 코드는
    비용 최적화를 위해 `gpt-3.5-turbo` 기본값을 유지한다. 책과 동일한 모델로
    실행하고 싶다면 아래처럼 `team.llm.model_name`을 지정한 뒤 호출하면 된다.

        team = CrewAITeam()
        team.llm.model_name = "gpt-4o-mini"
        team.process(...)
"""
import os
import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from crewai_agents import CrewAITeam


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        print("[오류] OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("        .env 파일이나 쉘 환경 변수에 키를 등록한 뒤 다시 실행해 주세요.")
        sys.exit(1)

    team = CrewAITeam()
    inquiry = "제품이 계속 멈추는데, 교환이나 환불이 가능한가요?"
    result = team.process(inquiry)

    print("\n" + "=" * 60)
    print("최종 결과")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
