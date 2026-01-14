"""
LangGraph 1단계: 상태 정의와 워크플로 구조
목표: 그래프 기반 워크플로의 뼈대 만들기
"""
import sys
from pathlib import Path

from langgraph.graph import StateGraph, END
from typing import TypedDict

# 상위 디렉토리의 llm_bridge 사용
sys.path.append(str(Path(__file__).parent.parent))
from llm_bridge import CachedLLMBridge


# LangGraph: 상태 정의와 워크플로 구조
class WorkflowState(TypedDict):
    """워크플로 전체에서 공유되는 상태"""  # ❶
    inquiry: str
    current_step: str
    tech_result: dict
    policy_result: dict
    final_response: str
    processing_path: list  # 어떤 경로로 처리되었는지 기록


class LangGraphWorkflow:
    """LangGraph를 사용한 조건부 워크플로"""

    def __init__(self):
        self.llm = CachedLLMBridge(provider="mock")
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """워크플로 그래프 구축"""  # ❷
        workflow = StateGraph(WorkflowState)

        # 노드 추가(각 노드는 하나의 작업)
        workflow.add_node("analyze", self.analyze_inquiry)
        workflow.add_node("technical", self.tech_analysis)
        workflow.add_node("policy", self.policy_check)
        workflow.add_node("finalize", self.create_response)

        # 시작점 설정
        workflow.set_entry_point("analyze")

        # 조건부 분기 추가
        workflow.add_conditional_edges(  # ❸
            "analyze",  # 시작 노드
            self.route_decision,  # 조건 함수
            {  # 가능한 경로
                "tech_only": "technical",
                "policy_only": "policy",
                "both": "technical",
                "end": "finalize"
            }
        )

        # 일반 에지 추가
        workflow.add_edge("technical", "policy")
        workflow.add_edge("policy", "finalize")
        workflow.add_edge("finalize", END)

        return workflow.compile()

    def route_decision(self, state):
        """다음 노드 결정"""  # ❹
        tech = state.get("tech_needed", False)
        policy = state.get("policy_needed", False)

        if tech and policy:
            return "both"
        elif tech:
            return "tech_only"
        elif policy:
            return "policy_only"
        else:
            return "end"

    # LangGraph: 노드 구현
    def analyze_inquiry(self, state):
        """문의 분석"""  # ❶
        inquiry = state["inquiry"]
        state["processing_path"] = ["analyze"]
        state["current_step"] = "analyzing"

        # 간단한 분석
        has_tech = any(word in inquiry for word in ["작동", "고장", "오류"])
        has_policy = any(word in inquiry for word in ["환불", "교환", "보증"])

        state["tech_needed"] = has_tech
        state["policy_needed"] = has_policy

        return state

    def tech_analysis(self, state):
        """기술 분석 수행"""  # ❷
        state["processing_path"].append("technical")

        prompt = f"기술 전문가로서 분석: {state['inquiry']}"
        response = self.llm._call(prompt)

        state["tech_result"] = {"analysis": response}
        state["current_step"] = "tech_completed"

        return state

    def policy_check(self, state):
        """정책 확인 수행"""  # ❸
        state["processing_path"].append("policy")

        tech_context = state.get("tech_result", {})
        prompt = f"""정책 확인:
        문의: {state['inquiry']}
        기술 분석: {tech_context.get('analysis', '없음')}
        """
        response = self.llm._call(prompt)

        state["policy_result"] = {"guidance": response}
        state["current_step"] = "policy_completed"

        return state

    def create_response(self, state):
        """최종 응답 생성"""  # ❹
        state["processing_path"].append("finalize")

        response = "고객님께 답변드립니다.\n\n"

        if state.get("tech_result"):
            response += f"【기술 진단】\n{state['tech_result']['analysis']}\n\n"

        if state.get("policy_result"):
            response += f"【정책 안내】\n{state['policy_result']['guidance']}\n\n"

        state["final_response"] = response
        state["current_step"] = "completed"

        return state

    # LangGraph: 실행 및 테스트
    def process(self, inquiry):
        """문의 처리"""
        initial_state = {  # ❶
            "inquiry": inquiry,
            "current_step": "start",
            "tech_result": {},
            "policy_result": {},
            "final_response": "",
            "processing_path": []
        }

        print(f"\n{'='*60}")
        print(f"LangGraph 워크플로 시작")
        print(f"문의: {inquiry}")
        print(f"{'='*60}\n")

        result = self.workflow.invoke(initial_state)  # ❷

        print(f"처리 경로: {' → '.join(result['processing_path'])}")
        print(f"{'='*60}\n")

        return result["final_response"]


# 테스트
if __name__ == "__main__":
    workflow = LangGraphWorkflow()

    test_cases = [
        "제품이 작동하지 않아요",
        "환불받고 싶어요",
        "고장 났는데 교환 가능한가요?"
    ]

    for inquiry in test_cases:
        result = workflow.process(inquiry)
        print(result)
