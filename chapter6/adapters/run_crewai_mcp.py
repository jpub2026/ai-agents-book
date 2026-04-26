"""
코드 6-18(`crewai_mcp_integration.py`)의 `create_mcp_enabled_crew()`를
실행해 MCPToolAdapter가 부착된 CrewAI Crew가 만들어지는지 확인하는
데모 스크립트.

책 본문에는 포함되지 않은 보조 실행 스크립트이며, 예제 코드 자체는 변경하지 않음.

필수 패키지:
    pip install crewai pydantic

실제 Crew를 `kickoff()` 하지 않고 Agent·Tool 구성만 점검한다. LLM 호출까지
시연하려면 `OPENAI_API_KEY` 등 모델 인증 정보가 추가로 필요하다.
"""
from crewai_mcp_integration import create_mcp_enabled_crew


def main() -> None:
    crew = create_mcp_enabled_crew()

    print("[CrewAI 팀 구성]")
    for agent in crew.agents:
        tool_names = [getattr(tool, "name", "unknown") for tool in agent.tools]
        print(f"  - {agent.role}: tools={tool_names}")

    print("[등록된 Task]")
    for task in crew.tasks:
        print(f"  - {task.description.strip().splitlines()[0][:60]}...")


if __name__ == "__main__":
    main()
