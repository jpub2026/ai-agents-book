from crewai import Agent, Task, Crew
from langchain.llms import OpenAI

def create_agent_team():
    """
    CrewAI로 협업하는 에이전트 팀을 구성합니다.
    
    우리가 만든 단일 에이전트를 여러 전문 에이전트로 확장한 것입니다.
    각 에이전트는 Planner, Executor 등의 역할을 전담합니다.
    """
    llm = OpenAI(temperature=0.7)
    
    # 에이전트 1: 분석가 (우리의 Planner와 유사)
    analyst = Agent(
        role='분석가',
        goal='사용자 요청을 분석하고 계획을 수립합니다',
        backstory='데이터 분석과 전략 수립의 전문가입니다',
        verbose=True,
        llm=llm
    )
    
    # 에이전트 2: 실행자 (우리의 Executor와 유사)
    executor = Agent(
        role='실행자',
        goal='계획을 실제로 실행하고 결과를 생성합니다',
        backstory='작업 실행과 도구 사용의 전문가입니다',
        verbose=True,
        llm=llm
    )
    
    # 에이전트 3: 품질 관리자 (추가적인 역할)
    quality_checker = Agent(
        role='품질 관리자',
        goal='실행 결과를 검토하고 개선점을 제안합니다',
        backstory='품질 보증과 최적화의 전문가입니다',
        verbose=True,
        llm=llm
    )
    
    # 작업 정의 - 각 에이전트가 수행할 작업 
    def create_meeting_prep_tasks(request: str):
        task1 = Task(
            description=f"요청 분석: {request}",
            agent=analyst,
            expected_output="구조화된 실행 계획"
        )
        
        task2 = Task(
            description="계획에 따라 작업 실행",
            agent=executor,
            expected_output="실행 결과 보고서"
        )
        
        task3 = Task(
            description="실행 결과 검토 및 최적화",
            agent=quality_checker,
            expected_output="최종 검토 보고서"
        )
        
        return [task1, task2, task3]
    
    # Crew 구성 - 에이전트들의 협업 팀 ❺
    crew = Crew(
        agents=[analyst, executor, quality_checker],
        tasks=create_meeting_prep_tasks("내일 회의 준비"),
        verbose=True
    )
    
    return crew

# 사용 예시
def run_agent_team():
    """에이전트 팀을 실행합니다"""
    crew = create_agent_team()
    result = crew.kickoff()  # 팀 작업 시작
    return result
