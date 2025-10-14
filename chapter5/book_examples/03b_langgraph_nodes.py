"""
LangGraph 2단계: 노드(작업) 구현
목표: 각 단계에서 state를 어떻게 수정하는지 이해
"""

class LangGraphWorkflow:
    # ... (이전 코드 계속)
    
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