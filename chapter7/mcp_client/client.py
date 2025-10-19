# /mcp_client/client.py
import httpx
from typing import Dict, Any
import uuid

class MCPClient:
    """MCP 서버와 통신하는 클라이언트"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):  # ❶
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)  # ❷
        self.tools = {}  # ❸
        
    async def discover_tools(self) -> Dict[str, Any]:
        """서버의 도구 목록 조회"""
        response = await self.client.get(f"{self.base_url}/mcp/tools")  # ❹
        response.raise_for_status()  # ❺
        
        data = response.json()
        
        # 도구 캐싱
        for tool in data["tools"]:  # ❻
            self.tools[tool["name"]] = tool
        
        return self.tools

    async def call_tool(
        self, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Any:
        """ 도구 호출 """
        
        # 도구 존재 확인 (캐시)
        if tool_name not in self.tools:  # ❶
            raise ValueError(f"Unknown tool: {tool_name}")
        
        # JSON-RPC 2.0 요청 생성
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": str(uuid.uuid4())  # ❷
        }
        
        # 서버에 요청
        response = await self.client.post(  # ❸
            f"{self.base_url}/mcp/execute",
            json=request
        )
        response.raise_for_status()
        
        data = response.json()
        
        # 에러 확인
        if "error" in data:  # ❹
            error_msg = data["error"].get("message", "Unknown error")
            raise Exception(f"MCP Error: {error_msg}")
        
        return data.get("result")
    
    async def close(self):
        """클라이언트 연결 종료"""
        await self.client.aclose()  # ❺

