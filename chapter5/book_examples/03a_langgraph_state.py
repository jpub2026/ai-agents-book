"""
LangGraph 1단계: 상태 정의와 워크플로우 구조
목표: 그래프 기반 워크플로우의 뼈대 만들기
"""
import sys
from pathlib import Path

from langgraph.graph import StateGraph, END
from typing import TypedDict

# 4장에서 만든 LLM 브리지 재사용
sys.path.append(str(Path(__file__).parent.parent.parent / 'chapter4'))
from step2_real_llm.cached_llm_bridge import CachedLLMBridge

class WorkflowState(TypedDict):
    """워크플로우 전체에서 공유되는 상태"""  # ❶
    inquiry: str
    current_step: str
    tech_result: dict
    policy_result: dict
    final_response: str
    processing_path: list  # 어떤 경로로 처리되었는지 기록

class LangGraphWorkflow:
    """LangGraph를 사용한 조건부 워크플로우"""
    
    def __init__(self):
        self.llm = CachedLLMBridge(provider="mock")
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        """워크플로우 그래프 구축"""  # ❷
        workflow = StateGraph(WorkflowState)
        
        # 노드 추가 (각 노드는 하나의 작업)
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
        
        # 일반 엣지 추가
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