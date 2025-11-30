"""
CrewAI 3단계: 팀 협업 실행
목표: 전문가들이 협력하여 문제 해결
"""
import sys
from pathlib import Path
import importlib.util

from crewai import Crew, Process

# 04b_crewai_tasks에서 클래스 가져오기
spec = importlib.util.spec_from_file_location(
    "crewai_tasks",
    Path(__file__).parent / "04b_crewai_tasks.py"
)
crewai_tasks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crewai_tasks)
CrewAITeamBase = crewai_tasks.CrewAITeam


class CrewAITeam(CrewAITeamBase):
    """실행 기능이 추가된 CrewAI 팀"""

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