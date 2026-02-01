# /mcp_client/client.py
import httpx
import ollama
import json
from typing import Dict, Any, List, Optional
import uuid

class MCPClient:
    """MCP 서버와 통신하는 클라이언트"""

    def __init__(self, base_url: str = "http://localhost:8000"):  
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)  
        self.tools = {}  

    async def discover_tools(self) -> Dict[str, Any]:
        """서버의 도구 목록 조회"""
        response = await self.client.get(f"{self.base_url}/mcp/tools")  
        response.raise_for_status()  

        data = response.json()

        # 도구 캐싱
        for tool in data["tools"]:  
            self.tools[tool["name"]] = tool

        return self.tools

    async def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Any:
        """ 도구 호출 """

        # 도구 존재 확인 (캐시)
        if tool_name not in self.tools:  
            raise ValueError(f"Unknown tool: {tool_name}")

        # JSON-RPC 2.0 요청 생성
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": str(uuid.uuid4())  
        }

        # 서버에 요청
        response = await self.client.post(  
            f"{self.base_url}/mcp/execute",
            json=request
        )
        response.raise_for_status()

        data = response.json()

        # 에러 확인 (error가 null이 아닌 경우만)
        if data.get("error"):  
            error_msg = data["error"].get("message", "Unknown error")
            raise Exception(f"MCP Error: {error_msg}")

        return data.get("result")

    def get_tools_for_ollama(self) -> List[Dict[str, Any]]:
        """Ollama 도구 호출 형식으로 도구 목록 반환"""
        ollama_tools = []
        for name, tool in self.tools.items():
            ollama_tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            })
        return ollama_tools

    async def close(self):
        """클라이언트 연결 종료"""
        await self.client.aclose()  


class OllamaAgent:
    """Ollama 기반 LLM 에이전트 - MCP 도구를 사용하여 작업 수행"""

    def __init__(
        self,
        mcp_client: MCPClient,
        model: str = "llama3.2",
        system_prompt: Optional[str] = None
    ):
        self.mcp_client = mcp_client
        self.model = model
        self.ollama_client = ollama.AsyncClient()
        self.system_prompt = system_prompt or self._default_system_prompt()
        self.conversation_history: List[Dict[str, Any]] = []

    def _default_system_prompt(self) -> str:
        return """당신은 고객 서비스 및 주문 처리를 담당하는 AI 에이전트입니다.

사용 가능한 도구를 활용하여 다음 작업을 수행할 수 있습니다:
1. get_customer: 고객 정보 조회 (구매 이력, 등급, 신용도 포함)
2. process_order: 새로운 주문 처리 (재고 확인, 결제, 배송 준비)
3. generate_report: 판매 보고서 생성 (매출, 주문량, 인기 상품 분석)

항상 친절하고 정확하게 응답하며, 필요한 경우 적절한 도구를 사용하세요.
도구 호출 결과를 바탕으로 사용자에게 명확한 답변을 제공하세요."""

    async def _execute_tool_calls(
        self,
        tool_calls: List[Any]
    ) -> List[Dict[str, Any]]:
        """도구 호출 실행 및 결과 반환"""
        results = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name

            # arguments가 문자열인 경우 JSON 파싱
            arguments = tool_call.function.arguments
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {}

            print(f"  [도구 호출] {function_name}")
            print(f"    인자: {json.dumps(arguments, ensure_ascii=False, indent=2)}")

            try:
                result = await self.mcp_client.call_tool(function_name, arguments)
                results.append({
                    "tool_name": function_name,
                    "success": True,
                    "result": result
                })
                print(f"    결과: 성공")
            except Exception as e:
                results.append({
                    "tool_name": function_name,
                    "success": False,
                    "error": str(e)
                })
                print(f"    결과: 실패 - {e}")

        return results

    async def run(self, user_message: str, max_iterations: int = 5) -> str:
        """
        사용자 메시지에 대해 에이전트 루프 실행

        Args:
            user_message: 사용자 입력 메시지
            max_iterations: 최대 반복 횟수 (무한 루프 방지)

        Returns:
            최종 응답 텍스트
        """
        # 도구 목록 가져오기
        tools = self.mcp_client.get_tools_for_ollama()

        # 대화 기록 초기화 (새 대화 시작)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]

        print(f"\n{'='*60}")
        print(f"[사용자 요청] {user_message}")
        print(f"{'='*60}")

        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            print(f"\n[반복 {iteration}/{max_iterations}]")

            # Ollama API 호출
            response = await self.ollama_client.chat(
                model=self.model,
                messages=messages,
                tools=tools if tools else None
            )

            assistant_message = response.message

            # 도구 호출이 있는 경우
            if assistant_message.tool_calls:
                print(f"  LLM이 {len(assistant_message.tool_calls)}개의 도구를 호출합니다...")

                # 도구 호출 정보 준비 (Ollama 형식)
                tool_calls_for_message = []
                for i, tc in enumerate(assistant_message.tool_calls):
                    # arguments가 문자열인 경우 dict로 변환
                    args = tc.function.arguments
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}

                    tool_calls_for_message.append({
                        "function": {
                            "name": tc.function.name,
                            "arguments": args  # dict 형태로 전달
                        }
                    })

                # 어시스턴트 메시지 추가
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": tool_calls_for_message
                })

                # 도구 실행
                tool_results = await self._execute_tool_calls(assistant_message.tool_calls)

                # 도구 결과를 메시지에 추가
                for i, result in enumerate(tool_results):
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(result, ensure_ascii=False, default=str)
                    })
            else:
                # 도구 호출 없음 - 최종 응답
                final_response = assistant_message.content or "응답을 생성할 수 없습니다."
                print(f"\n[최종 응답]")
                print(f"{final_response}")

                # 대화 기록 저장
                self.conversation_history = messages

                return final_response

        return "최대 반복 횟수에 도달했습니다. 작업을 완료하지 못했습니다."

