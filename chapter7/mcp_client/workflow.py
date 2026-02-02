# /mcp_client/workflow.py
from langgraph.graph import StateGraph, END
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, TYPE_CHECKING
import uuid
import json
import ollama

if TYPE_CHECKING:
    from client import MCPClient


@dataclass
class AgentState:
    """Ollama 에이전트 워크플로 상태"""
    messages: List[Dict[str, Any]] = field(default_factory=list)  # 대화 기록
    tools: List[Dict[str, Any]] = field(default_factory=list)  # 사용 가능한 도구
    tool_results: List[Dict[str, Any]] = field(default_factory=list)  # 도구 실행 결과
    final_response: str = ""  # 최종 응답
    iteration: int = 0  # 현재 반복 횟수
    max_iterations: int = 10  # 최대 반복 횟수
    should_continue: bool = True  # 계속 진행 여부


class OllamaWorkflow:
    """Ollama 기반 LLM 에이전트 워크플로 - LangGraph 사용"""

    def __init__(
        self,
        mcp_client: "MCPClient",
        model: str = "llama3.2"
    ):
        self.mcp_client = mcp_client
        self.model = model
        self.ollama_client = ollama.AsyncClient()
        self.workflow_id = str(uuid.uuid4())[:8]

        self.system_prompt = """당신은 고객 서비스 및 주문 처리를 담당하는 AI 에이전트입니다.

사용 가능한 도구를 활용하여 다음 작업을 수행할 수 있습니다:
1. get_customer: 고객 정보 조회 (구매 이력, 등급, 신용도 포함)
2. process_order: 새로운 주문 처리 (재고 확인, 결제, 배송 준비)
3. generate_report: 판매 보고서 생성 (매출, 주문량, 인기 상품 분석)

항상 친절하고 정확하게 응답하며, 필요한 경우 적절한 도구를 사용하세요.
도구 호출 결과를 바탕으로 사용자에게 명확한 답변을 제공하세요."""

    async def llm_node(self, state: AgentState) -> AgentState:
        """LLM 호출 노드 - Ollama API 사용"""
        print(f"[워크플로 {self.workflow_id}] LLM 노드 실행 (반복 {state.iteration + 1})")

        state.iteration += 1

        # Ollama API 호출
        response = await self.ollama_client.chat(
            model=self.model,
            messages=state.messages,
            tools=state.tools if state.tools else None
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
            state.messages.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": tool_calls_for_message
            })

            # 도구 호출 정보 저장
            state.tool_results = []
            for tc in assistant_message.tool_calls:
                state.tool_results.append({
                    "name": tc.function.name,
                    "arguments": tc.function.arguments
                })

            state.should_continue = True
        else:
            # 도구 호출 없음 - 최종 응답
            state.final_response = assistant_message.content or "응답을 생성할 수 없습니다."
            state.should_continue = False
            print(f"  최종 응답 생성 완료")

        return state

    async def tool_node(self, state: AgentState) -> AgentState:
        """도구 실행 노드 - MCP 서버를 통해 도구 호출"""
        print(f"[워크플로 {self.workflow_id}] 도구 노드 실행")

        for tool_call in state.tool_results:
            function_name = tool_call["name"]
            arguments = tool_call["arguments"]

            # arguments가 문자열인 경우 JSON 파싱
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {}

            print(f"  [도구 호출] {function_name}")
            print(f"    인자: {json.dumps(arguments, ensure_ascii=False, indent=2)}")

            try:
                result = await self.mcp_client.call_tool(function_name, arguments)
                tool_result = {
                    "tool_name": function_name,
                    "success": True,
                    "result": result
                }
                print(f"    결과: 성공")
            except Exception as e:
                tool_result = {
                    "tool_name": function_name,
                    "success": False,
                    "error": str(e)
                }
                print(f"    결과: 실패 - {e}")

            # 도구 결과를 메시지에 추가
            state.messages.append({
                "role": "tool",
                "content": json.dumps(tool_result, ensure_ascii=False, default=str)
            })

        # 도구 결과 초기화
        state.tool_results = []

        return state

    def should_continue(self, state: AgentState) -> str:
        """조건부 엣지 - 계속 진행할지 결정"""
        if not state.should_continue:
            return "end"
        if state.iteration >= state.max_iterations:
            print(f"  최대 반복 횟수 도달 ({state.max_iterations})")
            return "end"
        return "continue"

    def create_workflow(self) -> StateGraph:
        """워크플로 생성"""
        workflow = StateGraph(AgentState)  

        # 노드 추가
        workflow.add_node("llm", self.llm_node)  # LLM 호출 노드
        workflow.add_node("tools", self.tool_node)  #  도구 실행 노드

        # 진입점 설정
        workflow.set_entry_point("llm") 

        # 조건부 에지: LLM 노드 이후
        workflow.add_conditional_edges(  
            "llm",
            self.should_continue,
            {
                "continue": "tools",  # 도구 호출 필요
                "end": END  # 최종 응답 완료
            }
        )

        # 도구 노드 이후 다시 LLM 노드로
        workflow.add_edge("tools", "llm")  

        return workflow.compile()  

    async def run(self, user_message: str) -> str:
        """워크플로 실행"""
        print(f"\n{'='*60}")
        print(f"[사용자 요청] {user_message}")
        print(f"{'='*60}")

        # 도구 목록 가져오기
        tools = []
        for name, tool in self.mcp_client.tools.items():
            tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            })

        # 초기 상태 설정
        initial_state = AgentState(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ],
            tools=tools
        )

        # 워크플로 생성 및 실행
        workflow = self.create_workflow()
        final_state = await workflow.ainvoke(initial_state)

        # LangGraph는 dict를 반환할 수 있음
        if isinstance(final_state, dict):
            final_response = final_state.get("final_response", "응답 없음")
        else:
            final_response = final_state.final_response

        print(f"\n{'='*60}")
        print(f"[최종 응답]")
        print(final_response)
        print(f"{'='*60}")

        return final_response


# 하위 호환성을 위한 기존 클래스 유지 (레거시)
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
        workflow = StateGraph(WorkflowState)

        workflow.add_node("fetch_customer", self.fetch_customer_node)
        workflow.add_node("process_order", self.process_order_node)
        workflow.add_node("generate_report", self.generate_report_node)

        workflow.set_entry_point("fetch_customer")

        workflow.add_conditional_edges(
            "fetch_customer",
            lambda state: "continue" if state.customer_data else "end",
            {"continue": "process_order", "end": END}
        )

        workflow.add_conditional_edges(
            "process_order",
            lambda state: "continue" if state.order_data and state.order_data.get("success") else "end",
            {"continue": "generate_report", "end": END}
        )

        workflow.add_edge("generate_report", END)

        return workflow.compile()
