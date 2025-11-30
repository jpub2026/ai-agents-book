from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from pydantic import Field

class MCPToolAdapter(BaseTool):
    """MCP 서버를 CrewAI Tool로 사용하기 위한 어댑터"""
    name: str = "mcp_tool"
    description: str = "MCP 서버와 통신하는 도구"
    mcp_server_config: dict = Field(default_factory=dict)
    
    def _run(self, query: str) -> str:
        """도구 실행 메서드 - MCP 서버를 호출합니다"""
        mcp_request = {
            "jsonrpc": "2.0",
            "method": self.mcp_server_config.get("method", "execute"),
            "params": {"query": query},
            "id": 1
        }
        response = self._call_mcp_server(mcp_request)
        return f"MCP 서버 응답: {response}"

    def _call_mcp_server(self, request: dict) -> dict:
        """MCP 서버와 실제 통신 (시뮬레이션)"""
        # 실제 구현에서는 subprocess나 websocket 사용
        return {"jsonrpc": "2.0", "result": {"status": "success"}, "id": 1}

def create_mcp_enabled_crew():
    """MCP 도구를 사용하는 CrewAI 팀 생성"""
    
    # MCP 도구 생성
    file_tool = MCPToolAdapter(
        name="file_manager",
        description="파일 시스템을 관리하는 MCP 도구",
        mcp_server_config={
            "command": "npx",
            "args": ["@modelcontextprotocol/server-filesystem"],
            "method": "files/read"
        }
    )
    
    # 에이전트 생성: MCP 도구 사용
    researcher = Agent(
        role='Research Analyst',
        goal='파일과 데이터베이스에서 필요한 정보를 수집',
        tools=[file_tool],
        verbose=True
    )
    
    # 작업 정의
    research_task = Task(
        description="프로젝트 폴더에서 관련 문서들을 찾으세요",
        agent=researcher,
        expected_output="수집된 데이터와 문서 목록"
    )
    
    # Crew 생성
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential
    )
    
    return crew
