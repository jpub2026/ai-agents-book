import json
from typing import Dict, List, Any
# 코드 2-6의 통합 LLM 인터페이스를 불러옵니다.
import sys
sys.path.append('../chapter2')  # 2장 코드 경로 추가
from llm_interface import LLM

class Planner:
    """
    에이전트의 계획 수립을 담당하는 클래스
    복잡한 작업을 실행 가능한 단계들로 분해합니다
    """
    
    def __init__(self, llm=None):
        # 통합 LLM 인터페이스 사용 - llm이 없으면 자동 생성 
        self.llm = llm or LLM()  # 자동으로 최적의 제공자 선택
        
        self.planning_prompt_template = """
        당신은 작업 계획을 수립하는 전문가입니다.
        
        사용자 요청: {user_request}
        사용 가능한 도구: {available_tools}
        현재 상태: {current_context}
        
        이 요청을 완수하기 위한 단계별 계획을 수립하세요.
        각 단계는 구체적이고 실행 가능해야 합니다.
        
        출력 형식:
        {{
            "steps": [
                {{
                    "step_number": 1,
                    "description": "단계 설명",
                    "tool_required": "필요한 도구",
                    "expected_output": "예상 결과",
                    "dependencies": []  # 선행 단계 번호
                }}
            ],
            "estimated_time": "예상 소요 시간",
            "potential_risks": ["잠재적 위험 요소들"] 
        }}
        """
    
    def create_plan(self, user_request: str, available_tools: List[str], 
                   context: Dict = None) -> Dict:
        """
        사용자 요청에 대한 실행 계획을 생성합니다
        """
        # 프롬프트 준비
        prompt = self.planning_prompt_template.format(
            user_request=user_request,
            available_tools=", ".join(available_tools),
            current_context=context or "없음"
        )
        
        # 통합 LLM 인터페이스를 사용하여 계획 생성
        plan_response = self.llm.generate(
            prompt=prompt,
            temperature=0.3,  # 계획 수립은 일관성이 중요하므로 낮은 온도
            max_tokens=1000   # 충분한 길이의 계획을 위해
        )
        
        try:
            # JSON 파싱 시도
            plan = json.loads(plan_response)
            self.validate_plan(plan) # 계획 유효성 검사
            return plan
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 텍스트에서 JSON 추출 시도
            return self.extract_json_from_text(plan_response, user_request)
        except Exception as e:
            print(f"계획 생성 실패: {e}")
            return self.create_fallback_plan(user_request)

    def validate_plan(self, plan: Dict) -> bool:
        """계획의 유효성을 검증합니다"""
        required_fields = ['steps']
        for field in required_fields:
            if field not in plan:
                raise ValueError(f"필수 필드 누락: {field}")
        
        # 순환 의존성 검사
        for step in plan.get('steps', []):
            step_num = step.get('step_number')
            deps = step.get('dependencies', [])
            if step_num in deps:
                raise ValueError(f"순환 의존성 발견: 단계 {step_num}")
        
        return True
    
    def extract_json_from_text(self, text: str, user_request: str) -> Dict:
        """텍스트에서 JSON을 추출 시도"""
        try:
            # JSON 블록 찾기 시도
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except:
            pass
        return self.create_fallback_plan(user_request)
    
    def create_fallback_plan(self, user_request: str) -> Dict:
        """폴백 계획 생성"""
        return {
            "steps": [
                {
                    "step_number": 1,
                    "description": f"'{user_request}' 처리",
                    "tool_required": "general",
                    "expected_output": "작업 완료",
                    "dependencies": []
                }
            ],
            "estimated_time": "알 수 없음",
            "potential_risks": ["자동 생성된 기본 계획"]
        }
