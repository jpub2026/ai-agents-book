from langchain_core.tools import Tool
import json
import subprocess

# 참고: LangChain 에이전트 사용 시 필요한 import (주석 처리된 예제용)
# from langchain.agents import create_react_agent, AgentExecutor

class MCPToLangChainAdapter:
    """
    MCP 서버를 LangChain Tool로 변환하는 어댑터
    """
    
    def __init__(self, mcp_server_command: str, mcp_server_args: list):
        self.server_command = mcp_server_command
        self.server_args = mcp_server_args
        
    def call_mcp_server(self, method: str, params: dict) -> dict:
        """MCP 서버에 JSON-RPC 요청을 보내고 응답을 받습니다"""
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        # 실제 구현에서는 프로세스 간 통신 사용
        response = self._send_to_mcp_server(request)
        return response
    
    def _send_to_mcp_server(self, request: dict) -> dict:
        """MCP 서버와 실제 통신하는 핵심 메서드"""
        # JSON-RPC 요청을 LSP 형식으로 전송
        request_str = json.dumps(request)
        message = f"Content-Length: {len(request_str)}\r\n\r\n{request_str}"
        
        # subprocess를 통한 통신(간략화된 구현)
        # 실제로는 더 복잡한 프로세스 관리가 필요
        return {"jsonrpc": "2.0", "result": {"status": "success"}, "id": 1}
    
    def create_langchain_tool(self, tool_name: str, tool_description: str) -> Tool:
        """MCP 서버 기능을 LangChain Tool로 변환"""
        def tool_func(query: str) -> str:
            params = {"query": query}
            result = self.call_mcp_server("execute", params)
            return json.dumps(result, ensure_ascii=False)
        
        return Tool(
            name=tool_name,
            func=tool_func,
            description=tool_description
        )

# 사용 예제
def demonstrate_langchain_mcp_integration():
    """LangChain에서 MCP 서버를 사용하는 실제 예제"""
    # MCP 서버를 LangChain Tool로 변환
    mcp_adapter = MCPToLangChainAdapter(
        mcp_server_command="npx",
        mcp_server_args=["-y", "@modelcontextprotocol/server-filesystem"]
    )
    
    # 파일 시스템 접근 Tool 생성
    file_tool = mcp_adapter.create_langchain_tool(
        tool_name="file_reader",
        tool_description="파일 시스템에서 파일을 읽고 내용을 반환합니다"
    )
    
    # LangChain 에이전트에서 사용 (실제 사용 시 LLM 인스턴스 필요)
    # from langchain.llms import OpenAI
    # llm = OpenAI(temperature=0.7)
    # agent = initialize_agent(
    #     tools=[file_tool],
    #     llm=llm,
    #     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    # )
    print(f"Created MCP tool: {file_tool.name}")
    return file_tool

# 별칭 (호환성)
LangChainMCPAdapter = MCPToLangChainAdapter
