"""
CrewAI 3단계: 팀 협업 실행
목표: 전문가들이 협력하여 문제 해결
"""

from crewai import Crew, Process

class CrewAITeam:
    # ... (이전 코드 계속)
    
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