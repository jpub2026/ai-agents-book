"""
CrewAI 2단계: 작업(Task) 정의
목표: 각 전문가가 수행할 구체적인 작업 명세
"""
import sys
from pathlib import Path
import importlib.util

from crewai import Task

# 04a_crewai_agents에서 클래스 가져오기
spec = importlib.util.spec_from_file_location(
    "crewai_agents",
    Path(__file__).parent / "04a_crewai_agents.py"
)
crewai_agents = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crewai_agents)
CrewAITeamBase = crewai_agents.CrewAITeam


class CrewAITeam(CrewAITeamBase):
    """작업 정의가 추가된 CrewAI 팀"""

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