"""
LangGraph 3단계: 워크플로우 실행
목표: 실제로 동작하는 모습 확인
"""

class LangGraphWorkflow:
    # ... (이전 코드 계속)
    
    def process(self, inquiry):
        """문의 처리"""
        initial_state = {
            "inquiry": inquiry,
            "current_step": "start",
            "tech_result": {},
            "policy_result": {},
            "final_response": "",
            "processing_path": []
        }
        
        print(f"\n{'='*60}")
        print(f"LangGraph 워크플로우 시작")
        print(f"문의: {inquiry}")
        print(f"{'='*60}\n")
        
        result = self.workflow.invoke(initial_state) #❶
        
        print(f"처리 경로: {' → '.join(result['processing_path'])}")
        print(f"{'='*60}\n")
        
        return result["final_response"]

# 테스트
if __name__ == "__main__":
    workflow = LangGraphWorkflow()
    
    test_cases = [
        "제품이 작동하지 않아요",
        "환불 받고 싶어요",
        "고장났는데 교환 가능한가요?"
    ]
    
    for inquiry in test_cases:
        result = workflow.process(inquiry)
        print(result)