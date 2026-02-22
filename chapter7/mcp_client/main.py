# /mcp_client/main.py
import asyncio
from client import MCPClient, OllamaAgent
from workflow import MCPWorkflow, WorkflowState


async def run_ollama_agent_example():
    """Ollama 에이전트 실행 예제 - 간단한 에이전트 루프"""

    # MCP 클라이언트 초기화
    mcp_client = MCPClient()

    try:
        # 도구 발견
        print("MCP 서버에서 도구 목록을 가져오는 중...")
        tools = await mcp_client.discover_tools()
        print(f"발견된 도구: {list(tools.keys())}")

        # Ollama 에이전트 생성
        agent = OllamaAgent(mcp_client, model="llama3.2")

        # 다양한 요청 테스트
        test_queries = [
            "VIP-12345 고객의 정보를 조회해주세요.",
            "오늘의 판매 보고서를 생성해주세요.",
        ]

        for query in test_queries:
            response = await agent.run(query)
            print(f"\n{'='*60}\n")

    finally:
        await mcp_client.close()


async def run_workflow_example():
    """워크플로우 실행 예제 - LangGraph 기반 순차 워크플로"""

    # MCP 클라이언트 초기화
    mcp_client = MCPClient()

    try:
        # 도구 발견
        await mcp_client.discover_tools()

        # 워크플로우 생성
        workflow_manager = MCPWorkflow(mcp_client)
        workflow = workflow_manager.create_workflow()

        # 초기 상태 설정
        initial_state = WorkflowState(customer_id="VIP-12345")

        # 워크플로우 실행
        result = await workflow.ainvoke(initial_state)

        # LangGraph는 dict를 반환할 수 있음
        if isinstance(result, dict):
            errors = result.get("errors", [])
            customer_data = result.get("customer_data")
            order_data = result.get("order_data")
            report_data = result.get("report_data")
        else:
            errors = result.errors
            customer_data = result.customer_data
            order_data = result.order_data
            report_data = result.report_data

        # 결과 출력
        if errors:
            print("발생한 오류:")
            for error in errors:
                print(f"  - {error}")

        if customer_data:
            print(f"\n고객: {customer_data.get('name')}")
            print(f"등급: {customer_data.get('tier')}")

        if order_data:
            print(f"\n주문 ID: {order_data.get('order_id')}")
            pricing = order_data.get('pricing', {})
            if pricing:
                print(f"총액: {pricing.get('total', 0):,}원")

        if report_data:
            print(f"\n보고서 ID: {report_data.get('report_id')}")

    finally:
        await mcp_client.close()


if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("MCP 클라이언트 - Ollama 에이전트 예제")
    print("=" * 60)
    print("\n실행 모드 선택:")
    print("  1. Ollama 에이전트 (기본) - 간단한 에이전트 루프")
    print("  2. MCP 워크플로우 - LangGraph 기반 순차 워크플로")
    print()

    # 명령줄 인자로 모드 선택
    mode = sys.argv[1] if len(sys.argv) > 1 else "1"

    if mode == "1":
        print(">>> Ollama 에이전트 모드로 실행합니다...\n")
        asyncio.run(run_ollama_agent_example())
    elif mode == "2":
        print(">>> MCP 워크플로우 모드로 실행합니다...\n")
        asyncio.run(run_workflow_example())
    else:
        print(f"알 수 없는 모드: {mode}")
        print("사용법: python main.py [1|2]")
