import json
import asyncio
import websockets
from typing import Any, Dict, Optional
import uuid
from datetime import datetime

class MCPUnifiedApproach:
    """
    MCP를 사용한 통합된 AI 서비스 접근
    모든 서비스를 동일한 JSON-RPC 프로토콜로 호출
    """
    
    def __init__(self, host_url: str = "ws://localhost:8080"):
        self.host_url = host_url
        self.websocket = None
        self.pending_requests = {}
        
    async def connect(self):
        """MCP Host에 연결"""
        self.websocket = await websockets.connect(self.host_url)
        # 연결 후 백그라운드에서 응답 수신 시작
        asyncio.create_task(self._receive_messages())
        
    async def _receive_messages(self):
        """응답 메시지를 비동기로 수신"""
        async for message in self.websocket:
            data = json.loads(message)
            request_id = data.get("id")
            
            if request_id in self.pending_requests:
                # 대기 중인 요청에 응답 전달
                self.pending_requests[request_id].set_result(data)
                
    async def call_any_ai_service(
        self, 
        service_name: str, 
        method: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """통합된 방식으로 모든 AI 서비스 호출"""
        
        request_id = self.generate_request_id()
        
        # JSON-RPC 2.0 표준 형식의 요청 생성
        request = {
            "jsonrpc": "2.0",
            "method": f"{service_name}.{method}",
            "params": params,
            "id": request_id
        }
        
        # 응답을 기다릴 Future 생성
        future = asyncio.Future()
        self.pending_requests[request_id] = future
        
        # 요청 전송
        await self.websocket.send(json.dumps(request))

        # 응답 대기 (타임아웃 설정)
        try:
            response = await asyncio.wait_for(future, timeout=30.0)
            return response
        except asyncio.TimeoutError:
            del self.pending_requests[request_id]
            raise TimeoutError(f"Request {request_id} timed out")
    
    def generate_request_id(self) -> str:
        """고유한 요청 ID 생성"""
        timestamp = int(datetime.now().timestamp() * 1000000)
        unique_id = str(uuid.uuid4())[:8]
        return f"req_{timestamp}_{unique_id}"
    
    async def query_ai(self, service: str, prompt: str) -> str:
        """AI 서비스에 통합된 방식으로 질의"""
        response = await self.call_any_ai_service(
            service_name=service,
            method="complete",
            params={"prompt": prompt}
        )
        
        # 통합된 응답 처리
        if "result" in response:
            return response["result"].get("text", "")
        elif "error" in response:
            raise Exception(f"Service error: {response['error']['message']}")
        return ""
    
    async def close(self):
        """연결 종료"""
        if self.websocket:
            await self.websocket.close()

# 실제 사용 예제
async def main():
    mcp_client = MCPUnifiedApproach()
    await mcp_client.connect()
    
    try:
        # 모든 서비스를 동일한 방식으로 호출
        services = ["openai", "claude", "gemini"]
        prompt = "What is MCP protocol?"
        
        for service in services:
            try:
                response = await mcp_client.query_ai(service, prompt)
                print(f"\n{service.upper()} Response:")
                print(response[:200] + "..." if len(response) > 200 else response)
            except Exception as e:
                print(f"{service.upper()} Error: {e}")
                
    finally:
        await mcp_client.close()

if __name__ == "__main__":
    asyncio.run(main())
