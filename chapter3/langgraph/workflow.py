from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator

class AgentState(TypedDict):
    """
    에이전트의 상태를 정의합니다.
    
    이는 우리가 만든 작업 기억(working memory)와 비슷한 개념입니다.
    워크플로우 전체에서 공유되는 상태입니다.
    """
    messages: Annotated[Sequence[str], operator.add]
    current_step: str
    plan: list
    results: dict

def create_langgraph_agent():
    """
    LangGraph로 복잡한 에이전트 워크플로우를 구성합니다.
    
    우리가 구현한 의존성 관리와 병렬 처리를
    그래프 구조로 더 명확하게 표현할 수 있습니다.
    """
    # 워크플로우 그래프 생성
    workflow = StateGraph(AgentState)
    
    # 노드 정의 - 우리의 각 단계와 대응
    def analyze_request(state: AgentState) -> AgentState:
        """1단계: 요청 분석 (Memory 검색과 유사)"""
        state["current_step"] = "analyzing"
        # 요청 분석 로직
        return state
    
    def create_plan(state: AgentState) -> AgentState:
        """2단계: 계획 수립 (Planner와 유사)"""
        state["current_step"] = "planning"
        state["plan"] = ["task1", "task2", "task3"]
        return state
    
    def execute_plan(state: AgentState) -> AgentState:
        """3단계: 실행 (Executor와 유사)"""
        state["current_step"] = "executing"
        # 계획 실행 로직
        return state
    
    def save_experience(state: AgentState) -> AgentState:
        """4단계: 경험 저장 (Memory 저장과 유사)"""
        state["current_step"] = "saving"
        # 경험 저장 로직
        return state

    # 노드 추가
    workflow.add_node("analyze", analyze_request)
    workflow.add_node("plan", create_plan)
    workflow.add_node("execute", execute_plan)
    workflow.add_node("save", save_experience)
    
    # 엣지 정의 - 조건부 분기 가능
    def should_replan(state: AgentState) -> str:
        """실행 결과에 따라 재계획이 필요한지 결정"""
        if state.get("results", {}).get("success", False):
            return "save"  # 성공하면 저장으로
        else:
            return "plan"  # 실패하면 재계획으로
    
    workflow.add_edge("analyze", "plan")
    workflow.add_edge("plan", "execute")
    workflow.add_conditional_edges(
        "execute",
        should_replan,
        {
            "save": "save",
            "plan": "plan"  # 다시 계획으로 돌아감
        }
    )
    workflow.add_edge("save", END)
    
    # 시작점 설정
    workflow.set_entry_point("analyze")

    # 컴파일하여 실행 가능한 에이전트로 변환
    app = workflow.compile()
    
    return app
