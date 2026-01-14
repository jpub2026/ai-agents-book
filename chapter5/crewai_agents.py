"""
CrewAI를 사용한 고객 서비스 팀

설치 필요: pip install crewai langchain-openai python-dotenv
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# OpenAI API 키 설정 (아래 방법 중 하나 선택)
# 방법 1: 환경변수 직접 설정
# import os
# os.environ["OPENAI_API_KEY"] = "sk-your-api-key-here"

# 방법 2: .env 파일 사용 (권장)
# from dotenv import load_dotenv
# load_dotenv()  # 프로젝트 루트의 .env 파일에서 로드

# .env 파일 예시:
# OPENAI_API_KEY=sk-your-api-key-here


# CrewAI - 에이전트 정의
class CrewAITeam:
    """CrewAI를 사용한 고객 서비스 팀"""

    def __init__(self):
        # OpenAI LLM 초기화 (API 키 필요)
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3
            # api_key는 환경변수 OPENAI_API_KEY에서 자동으로 로드됨
        )
        self.agents = self._create_agents()

    def _create_agents(self):
        """에이전트 팀 구성"""  # ❶

        analyst = Agent(
            role='Customer Inquiry Analyst',  # ❷
            goal='고객 문의를 정확히 분석하고 분류하기',
            backstory="""당신은 5년 경력의 고객 서비스 분석가입니다.
            수천 건의 문의를 처리한 경험으로 고객의 진짜 니즈를 빠르게 파악합니다.
            문의 유형, 긴급도, 감정 상태를 정확히 분석하는 전문가입니다.""",  # ❸
            verbose=True,
            llm=self.llm
        )

        technical_expert = Agent(
            role='Technical Support Specialist',
            goal='기술 문제를 정확히 진단하고 해결책 제시',
            backstory="""당신은 10년 경력의 기술 지원 전문가입니다.
            하드웨어와 소프트웨어 모두에 정통하며, 복잡한 기술 문제도
            쉽게 설명하는 능력이 뛰어납니다.""",
            verbose=True,
            llm=self.llm
        )

        policy_advisor = Agent(
            role='Policy and Customer Service Advisor',
            goal='고객에게 가장 유리한 정책 옵션 제공',
            backstory="""당신은 회사 정책을 정통한 고객 서비스 전문가입니다.
            규정을 준수하면서도 고객 만족을 최우선으로 생각합니다.
            win-win 솔루션을 찾는 데 능숙합니다.""",
            verbose=True,
            llm=self.llm
        )

        return {
            "analyst": analyst,
            "technical": technical_expert,
            "policy": policy_advisor
        }

    # CrewAI - 작업 정의
    def _create_tasks(self, inquiry):
        """작업 목록 생성"""  # ❶

        # Task 1: 초기 분석
        analysis_task = Task(
            description=f"""
            다음 고객 문의를 분석하세요:
            "{inquiry}"

            분석 항목:
            1. 문의 유형 (기술/정책/일반)
            2. 긴급도 (높음/중간/낮음)
            3. 고객 감정 상태
            4. 핵심 요구사항

            구조화된 분석 결과를 제공하세요.
            """,
            expected_output="문의 유형, 긴급도, 감정 상태, 핵심 요구사항을 포함한 분석 보고서",
            agent=self.agents["analyst"]
        )

        # Task 2: 기술 진단
        technical_task = Task(
            description=f"""
            고객 문의에 대해 기술적 진단을 수행하세요.

            진단 내용:
            1. 문제의 기술적 원인 (하드웨어/소프트웨어/사용자 오류)
            2. 심각도 평가
            3. 권장 해결 방법
            4. 예상 처리 시간

            전문적이면서도 이해하기 쉽게 설명하세요.
            """,
            expected_output="기술 진단 결과와 권장 해결 방법",
            agent=self.agents["technical"],
            context=[analysis_task]  # ❷
        )

        # Task 3: 정책 확인 및 최종 제안
        policy_task = Task(
            description=f"""
            기술 진단 결과를 바탕으로 최적의 정책을 제안하세요.

            확인 사항:
            1. 적용 가능한 보증/교환/환불 정책
            2. 필요한 절차와 서류
            3. 고객에게 가장 유리한 옵션
            4. 예상 처리 기간

            고객 친화적이면서도 정확하게 안내하세요.
            """,
            expected_output="적용 가능한 정책과 고객 맞춤 제안",
            agent=self.agents["policy"],
            context=[analysis_task, technical_task]  # ❸
        )

        return [analysis_task, technical_task, policy_task]

    # CrewAI - 팀 실행
    def process(self, inquiry):
        """문의 처리"""
        print(f"\n{'='*60}")
        print(f"CrewAI 팀이 처리 시작")
        print(f"문의: {inquiry}")
        print(f"{'='*60}\n")

        crew = Crew(
            agents=list(self.agents.values()),
            tasks=self._create_tasks(inquiry),
            process=Process.sequential,  # ❶
            verbose=True
        )

        result = crew.kickoff()

        return result


# 테스트
if __name__ == "__main__":
    team = CrewAITeam()

    inquiry = "제품이 계속 멈추는데, 교환이나 환불이 가능한가요?"
    result = team.process(inquiry)

    print(f"\n{'='*60}")
    print("최종 결과:")
    print(f"{'='*60}")
    print(result)
