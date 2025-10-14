"""
CrewAI 1단계: 전문가 에이전트 정의
목표: 역할과 전문성을 가진 팀원 구성

설치 필요: pip install crewai langchain-openai python-dotenv
"""

from crewai import Agent
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