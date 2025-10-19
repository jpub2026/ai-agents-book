# /mcp_client/main.py
import asyncio

async def run_workflow_example():
    """워크플로우 실행 예제"""
    
    # MCP 클라이언트 초기화
    mcp_client = MCPClient()
    
    try:
        # 도구 발견
        await mcp_client.discover_tools()
        
        # 워크플로우 생성
        workflow_manager = MCPWorkflow(mcp_client)
        workflow = workflow_manager.create_workflow()
        
        # 초기 상태 설정
        initial_state = WorkflowState(customer_id="VIP-12345")  # ❶
        
        # 워크플로우 실행
        final_state = await workflow.ainvoke(initial_state)  # ❷
        
        # 결과 출력
        if final_state.errors:  # ❸
            print("발생한 오류:")
            for error in final_state.errors:
                print(f"  - {error}")
        
        if final_state.customer_data:  # ❹
            print(f"\n고객: {final_state.customer_data.get('name')}")
            print(f"등급: {final_state.customer_data.get('tier')}")
        
        if final_state.order_data:
            print(f"\n주문 ID: {final_state.order_data.get('order_id')}")
            print(f"총액: {final_state.order_data.get('pricing', {}).get('total'):,}원")
        
        if final_state.report_data:
            print(f"\n보고서 ID: {final_state.report_data.get('report_id')}")
        
    finally:
        await mcp_client.close()  # ❺

if __name__ == "__main__":
    asyncio.run(run_workflow_example())  # ❻
