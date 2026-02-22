# /mcp_client/workflow.py
from langgraph.graph import StateGraph, END
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, TYPE_CHECKING
import uuid
import json

if TYPE_CHECKING:
    from client import MCPClient


@dataclass
class WorkflowState:
    """워크플로 상태"""
    customer_id: str = ""
    customer_data: Optional[Dict] = None
    order_data: Optional[Dict] = None
    report_data: Optional[Dict] = None
    errors: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class MCPWorkflow:
    """MCP 도구를 사용하는 워크플로"""

    def __init__(self, mcp_client: "MCPClient"):
        self.mcp_client = mcp_client
        self.workflow_id = str(uuid.uuid4())[:8]

    async def fetch_customer_node(self, state: WorkflowState) -> WorkflowState:
        """1단계: 고객 정보 조회"""
        print(f"[워크플로 {self.workflow_id}] 1단계: 고객 정보 조회")

        try:
            if not state.customer_id:
                state.errors.append("No customer ID provided")
                return state
            # MCP 도구 호출
            result = await self.mcp_client.call_tool(
                "get_customer",
                {"customer_id": state.customer_id, "include_orders": True}
            )

            if result.get("success"):
                state.customer_data = result.get("data")
                state.metadata["customer_fetch_time"] = result.get("query_time_ms")
            else:
                state.errors.append(f"고객 조회 실패: {result.get('error')}")

        except Exception as e:
            state.errors.append(f"고객 조회 중 예외: {str(e)}")

        return state

    async def process_order_node(self, state: WorkflowState) -> WorkflowState:
        """2단계: 주문 처리"""
        print(f"[워크플로 {self.workflow_id}] 2단계: 주문 처리")

        # 선행 조건 확인
        if not state.customer_data:
            state.errors.append("No customer data for order processing")
            return state

        try:
            # 샘플 주문 데이터(실제로는 입력받음)
            order_params = {
                "customer_id": state.customer_id,
                "items": [
                    {"product_id": "PRD-001", "quantity": 2, "price": 50000},
                    {"product_id": "PRD-002", "quantity": 1, "price": 75000}
                ],
                "payment_method": "credit_card",
                "shipping_address": {
                    "street": "테헤란로 123",
                    "city": "서울",
                    "postal_code": "06234"
                }
            }

            result = await self.mcp_client.call_tool("process_order", order_params)

            if result.get("success"):
                state.order_data = result
                state.metadata["order_id"] = result.get("order_id")
            else:
                state.errors.append(f"주문 처리 실패: {result.get('error')}")

        except Exception as e:
            state.errors.append(f"주문 처리 중 예외: {str(e)}")

        return state

    async def generate_report_node(self, state: WorkflowState) -> WorkflowState:
        """3단계: 보고서 생성"""
        print(f"[워크플로 {self.workflow_id}] 3단계: 보고서 생성")

        if not state.order_data:
            state.errors.append("No order data for report generation")
            return state

        try:
            result = await self.mcp_client.call_tool(
                "generate_report",
                {"report_type": "daily", "format": "json", "include_charts": True}
            )

            if result.get("success"):
                state.report_data = result.get("report")
                state.metadata["report_id"] = result.get("report", {}).get("report_id")
            else:
                state.errors.append(f"보고서 생성 실패: {result.get('error')}")

        except Exception as e:
            state.errors.append(f"보고서 생성 중 예외: {str(e)}")

        return state

    def create_workflow(self) -> StateGraph:
        """워크플로 생성"""
        workflow = StateGraph(WorkflowState)  # ❶

        # 노드 추가
        workflow.add_node("fetch_customer", self.fetch_customer_node)
        workflow.add_node("process_order", self.process_order_node)
        workflow.add_node("generate_report", self.generate_report_node)

        # 진입점 설정
        workflow.set_entry_point("fetch_customer")  # ❷

        # 조건부 에지: 고객 데이터가 있으면 주문 처리로, 없으면 종료
        workflow.add_conditional_edges(  # ❸
            "fetch_customer",
            lambda state: "continue" if state.customer_data else "end",
            {"continue": "process_order", "end": END}
        )

        # 조건부 에지: 주문이 성공하면 보고서 생성으로, 아니면 종료
        workflow.add_conditional_edges(
            "process_order",
            lambda state: "continue" if state.order_data and state.order_data.get("success") else "end",
            {"continue": "generate_report", "end": END}
        )

        # 보고서 생성 후 종료
        workflow.add_edge("generate_report", END)  # ❹

        return workflow.compile()  # ❺
