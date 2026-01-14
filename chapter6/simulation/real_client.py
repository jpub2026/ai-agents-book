# 파트 1: 초기 설정과 연결 수립
import asyncio
import json
import websockets
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum

class MCPError(Exception):
    """MCP 관련 에러를 위한 커스텀 예외 클래스"""
    def __init__(self, code: int, message: str, data: Any = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"MCP Error {code}: {message}")

@dataclass
class MCPClient:
    """실제 MCP 통신을 수행하는 프로덕션 레디 클라이언트"""
    
    server_url: str = "ws://localhost:3000"
    websocket: Optional[websockets.WebSocketClientProtocol] = None
    message_id: int = 0
    capabilities: Dict[str, Any] = field(default_factory=dict)
    available_tools: List[Dict[str, Any]] = field(default_factory=list)
    is_initialized: bool = False
    
    async def connect(self):
        """서버에 WebSocket 연결 수립"""
        try:
            # WebSocket 연결 생성 ❶
            self.websocket = await websockets.connect(
                self.server_url,
                ping_interval=20,  # 20초마다 핑 전송
                ping_timeout=10,   # 10초 내 퐁 미수신 시 재연결
                close_timeout=10   # 종료 대기 시간
            )
            print(f"Connected to MCP server at {self.server_url}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MCP server: {e}")
    
    async def initialize(self) -> Dict[str, Any]:
        """MCP 프로토콜 초기화 핸드셰이크"""
        if not self.websocket:
            raise RuntimeError("Not connected to server. Call connect() first.")
        
        # 메시지 ID 생성 및 관리 ❷
        self.message_id += 1
        current_id = self.message_id
        
        # 초기화 요청 구성 ❸
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "1.0.0",
                "capabilities": {
                    "tools": True,      # 도구 실행 가능
                    "prompts": True,    # 프롬프트 템플릿 지원
                    "resources": True   # 리소스 접근 가능
                },
                "clientInfo": {
                    "name": "MCP Python Client",
                    "version": "1.0.0"
                }
            },
            "id": current_id
        }
        
        # 요청 전송 및 응답 대기 ❹
        await self.websocket.send(json.dumps(init_request))
        
        # 타임아웃 설정으로 응답 대기
        try:
            response = await asyncio.wait_for(
                self.websocket.recv(),
                timeout=5.0  # 5초 타임아웃
            )
        except asyncio.TimeoutError:
            raise TimeoutError("Server did not respond to initialization")
        
        response_data = json.loads(response)
        
        # 응답 검증 및 상태 업데이트 ❺
        if response_data.get("id") != current_id:
            raise MCPError(-1, "Response ID mismatch")
        
        if "error" in response_data:
            error = response_data["error"]
            raise MCPError(
                error.get("code", -1),
                error.get("message", "Unknown error"),
                error.get("data")
            )
        
        # 서버 capabilities 저장
        if "result" in response_data:
            result = response_data["result"]
            self.capabilities = result.get("capabilities", {})
            self.is_initialized = True
            
            print(f"Initialized with server: {result.get('serverInfo', {})}")
            print(f"Server capabilities: {list(self.capabilities.keys())}")
            
        return response_data
    
    # 파트 2: 도구 검색과 실행
    # 서버가 제공하는 도구를 탐색하고 안전하게 실행하는 메커니즘
    async def list_tools(self) -> List[Dict[str, Any]]:
        """사용 가능한 도구 목록 조회"""
        if not self.is_initialized:
            raise RuntimeError("Client not initialized. Call initialize() first.")

        # 도구 목록 요청
        self.message_id += 1
        current_id = self.message_id
        
        request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": current_id
        }
        
        await self.websocket.send(json.dumps(request))
        
        try:
            response = await asyncio.wait_for(
                self.websocket.recv(),
                timeout=5.0
            )
        except asyncio.TimeoutError:
            raise TimeoutError("Server did not respond to tools/list request")
        
        response_data = json.loads(response)
        
        # 도구 정보 파싱 및 검증 ❼
        if "result" in response_data:
            tools = response_data["result"].get("tools", [])
            self.available_tools = tools
            
            # 도구별 스키마 검증
            for tool in tools:
                if "inputSchema" not in tool:
                    print(f"Tool '{tool['name']}' has no input schema")
                else:
                    # 필수 파라미터 추출
                    required = tool["inputSchema"].get("required", [])
                    print(f"{tool['name']}: {tool.get('description', 'No description')}")
                    if required:
                        print(f"    Required params: {required}")
            
            return tools
        
        return []
    
    async def call_tool(
        self, 
        tool_name: str, 
        arguments: Dict[str, Any],
        timeout: float = 30.0
    ) -> Any:
        """도구 실행 및 결과 반환"""

        # 도구 가용성 검증
        available_tool_names = [tool["name"] for tool in self.available_tools]
        if tool_name not in available_tool_names:
            raise ValueError(
                f"Tool '{tool_name}' not available. "
                f"Available tools: {available_tool_names}"
            )
        
        # 도구 스키마 가져오기
        tool_schema = next(
            (t for t in self.available_tools if t["name"] == tool_name),
            None
        )
        
        # 입력 파라미터 검증
        if tool_schema and "inputSchema" in tool_schema:
            required_params = tool_schema["inputSchema"].get("required", [])
            missing_params = [p for p in required_params if p not in arguments]
            
            if missing_params:
                raise ValueError(
                    f"Missing required parameters for '{tool_name}': {missing_params}"
                )
        
        # 도구 실행 요청
        self.message_id += 1
        current_id = self.message_id
        
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": current_id
        }
        
        print(f"→ Calling tool '{tool_name}' with arguments: {arguments}")
        await self.websocket.send(json.dumps(request))
        
        # 결과 수신 및 처리
        try:
            response = await asyncio.wait_for(
                self.websocket.recv(),
                timeout=timeout  # 도구별로 다른 타임아웃 가능
            )
        except asyncio.TimeoutError:
            raise TimeoutError(
                f"Tool '{tool_name}' execution timed out after {timeout} seconds"
            )
        
        response_data = json.loads(response)
        
        # 에러 처리
        if "error" in response_data:
            error = response_data["error"]
            print(f"Tool execution failed: {error.get('message')}")
            
            # 사용 가능한 도구 목록 제공
            if error.get("code") == -32601:  # Method not found
                print(f"Available tools: {available_tool_names}")
            
            raise MCPError(
                error.get("code", -1),
                error.get("message", "Tool execution failed"),
                error.get("data")
            )
        
        # 성공 결과 반환
        result = response_data.get("result")
        print(f"Tool '{tool_name}' executed successfully")
        
        # 실행 시간이 있으면 표시
        if isinstance(result, dict) and "executionTime" in result:
            print(f"  Execution time: {result['executionTime']}")
        
        return result

    # 파트 3: 연결 종료와 실행 예제
    # 리소스 정리와 실제 사용 시나리오를 통한 전체 통합
    async def close(self):
        """연결 정리 및 리소스 해제"""
        if self.websocket:
            # 정상 종료 시퀀스 
            try:
                await self.websocket.close(code=1000, reason="Normal closure")
                print("Connection closed gracefully")
            except Exception as e:
                print(f"Error during connection closure: {e}")
            finally:
                self.websocket = None
                self.is_initialized = False
                self.available_tools = []
                self.capabilities = {}

# 실제 사용 예제
async def main():
    """MCP 클라이언트 실사용 시나리오"""
    
    client = MCPClient("ws://localhost:3000")
    
    try:
        # 1. 연결 수립 
        await client.connect()

        # 2. 프로토콜 초기화
        init_result = await client.initialize()
        server_info = init_result.get("result", {}).get("serverInfo", {})
        print(f"\nServer: {server_info.get('name')} v{server_info.get('version')}")
        
        # 3. 도구 발견
        print("\n=== Available Tools ===")
        tools = await client.list_tools()
        
        if not tools:
            print("No tools available")
            return

        # 4. 도구 실행 예제
        print("\n=== Executing Tools ===")
        
        # 데이터베이스 쿼리 실행
        if "database_query" in [t["name"] for t in tools]:
            result = await client.call_tool(
                "database_query",
                {"sql": "SELECT name, email FROM users WHERE active = true LIMIT 3"}
            )
            
            if isinstance(result, dict) and "rows" in result:
                print(f"\nQuery returned {result.get('rowCount', 0)} rows:")
                for row in result["rows"]:
                    print(f"  - {row.get('name')}: {row.get('email')}")
        
        # 파일 읽기 실행
        if "file_read" in [t["name"] for t in tools]:
            result = await client.call_tool(
                "file_read",
                {"path": "/config.json"}
            )
            print(f"\nFile content: {result}")
        
        # 5. 에러 케이스 테스트
        print("\n=== Error Handling Demo ===")
        try:
            await client.call_tool("non_existent_tool", {})
        except MCPError as e:
            print(f"Expected error caught: {e.message}")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # 6. 정리
        await client.close()

# 실행
if __name__ == "__main__":
    asyncio.run(main())
