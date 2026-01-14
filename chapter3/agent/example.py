import sys
from pathlib import Path

# 현재 디렉토리를 기준으로 경로 설정
sys.path.append(str(Path(__file__).parent))
from core import Agent


def main():
    """
    통합 Agent 클래스의 실제 사용 예제입니다.
    각 예제의 실행 과정을 시각화하여 이해를 돕습니다.
    """
    
    # Agent 생성 - 모든 구성요소가 자동으로 초기화됩니다
    print("AI 에이전트 시스템 시작...")
    agent = Agent()
    
    # 예제 1: 첫 번째 회의 준비
    response1 = agent.process_request("내일 오전 10시 회의 준비해줘")
    
    # 예제 2: 두 번째 회의 준비 (경험 활용)
    response2 = agent.process_request("다음 주 월요일 회의도 준비해줘")
    
    # 예제 3: 다른 종류의 요청
    response3 = agent.process_request("팀원들에게 프로젝트 현황 공유해줘")

if __name__ == "__main__":
    main()
