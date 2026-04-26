"""
코드 6-3·6-4(`mcp_unified_approach.py`)의 MCPUnifiedApproach 클래스를
실행하는 데모 스크립트.

책 본문에는 포함되지 않은 보조 실행 스크립트이며, 예제 코드 자체는 변경하지 않음.

필수 패키지:
    pip install websockets

사전 준비:
    ws://localhost:8080 으로 응답하는 JSON-RPC 2.0 호환 WebSocket
    서버가 필요하다. 준비된 서버가 없는 환경에서는 연결 단계에서
    ConnectionRefusedError가 발생하므로 이 경우에는 아래의 offline
    모드가 자동으로 실행된다.

실행:
    cd chapter6/examples
    python run_mcp_unified.py
"""
import asyncio

from mcp_unified_approach import MCPUnifiedApproach, main as demo_main


async def offline_demo() -> None:
    """MCP Host 없이도 메시지 생성 로직만 점검할 수 있는 간이 데모"""
    client = MCPUnifiedApproach()
    request_id = client.generate_request_id()
    sample_request = {
        "jsonrpc": "2.0",
        "method": "filesystem.execute",
        "params": {"query": "사용자 정보 조회"},
        "id": request_id,
    }
    print("[오프라인 모드] 생성된 JSON-RPC 요청 예시:")
    print(sample_request)


def main() -> None:
    try:
        asyncio.run(demo_main())
    except (ConnectionRefusedError, OSError) as e:
        print(f"[안내] MCP Host(ws://localhost:8080)에 연결할 수 없어 오프라인 데모로 전환합니다. ({e})")
        asyncio.run(offline_demo())


if __name__ == "__main__":
    main()
