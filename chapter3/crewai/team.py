"""
CrewAI로 협업하는 에이전트 팀을 구성하는 예제.

- 실행 전 `pip install crewai crewai-tools langchain-openai` 가 필요합니다.
- OPENAI_API_KEY 환경 변수가 있어야 실제로 동작합니다.
"""
import os
import sys


def create_agent_team(request: str = "내일 회의 준비"):
    """
    CrewAI로 협업하는 에이전트 팀을 구성합니다.

    우리가 만든 단일 에이전트를 여러 전문 에이전트로 확장한 것입니다.
    각 에이전트는 Planner, Executor 등의 역할을 전담합니다.
    """
    try:
        from crewai import Agent, Crew, Task
        from langchain_openai import OpenAI
    except ImportError as e:
        raise ImportError(
            "CrewAI 관련 패키지가 필요합니다. "
            "`pip install crewai crewai-tools langchain-openai` 로 설치해 주세요."
        ) from e

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

    llm = OpenAI(temperature=0.7)

    # 에이전트 1: 분석가 (Planner와 유사)
    analyst = Agent(
        role="분석가",
        goal="사용자 요청을 분석하고 계획을 수립합니다",
        backstory="데이터 분석과 전략 수립의 전문가입니다",
        verbose=True,
        llm=llm,
    )

    # 에이전트 2: 실행자 (Executor와 유사)
    executor = Agent(
        role="실행자",
        goal="계획을 실제로 실행하고 결과를 생성합니다",
        backstory="작업 실행과 도구 사용의 전문가입니다",
        verbose=True,
        llm=llm,
    )

    # 에이전트 3: 품질 관리자
    quality_checker = Agent(
        role="품질 관리자",
        goal="실행 결과를 검토하고 개선점을 제안합니다",
        backstory="품질 보증과 최적화의 전문가입니다",
        verbose=True,
        llm=llm,
    )

    tasks = [
        Task(
            description=f"요청 분석: {request}",
            agent=analyst,
            expected_output="구조화된 실행 계획",
        ),
        Task(
            description="계획에 따라 작업 실행",
            agent=executor,
            expected_output="실행 결과 보고서",
        ),
        Task(
            description="실행 결과 검토 및 최적화",
            agent=quality_checker,
            expected_output="최종 검토 보고서",
        ),
    ]

    crew = Crew(
        agents=[analyst, executor, quality_checker],
        tasks=tasks,
        verbose=True,
    )

    return crew


def run_agent_team(request: str = "내일 회의 준비"):
    """에이전트 팀을 실행합니다."""
    crew = create_agent_team(request)
    return crew.kickoff()


if __name__ == "__main__":
    try:
        result = run_agent_team()
    except (ImportError, EnvironmentError) as e:
        print(f"[안내] {e}")
        sys.exit(0)

    print(result)
