"""
조건부 협업 2단계: 필요한 에이전트만 실행
목표: 효율적인 리소스 활용
"""
import sys
from pathlib import Path
import importlib.util

# 이전 파일에서 클래스들 가져오기
sys.path.append(str(Path(__file__).parent))

# 01_basic_collaboration에서 에이전트 클래스들 가져오기
spec = importlib.util.spec_from_file_location(
    "basic_collaboration",
    Path(__file__).parent / "01_basic_collaboration.py"
)
basic_collab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(basic_collab)
TechnicalAgent = basic_collab.TechnicalAgent
PolicyAgent = basic_collab.PolicyAgent


class SmartCoordinator:
    """문의 유형을 분석하여 적절한 에이전트 선택"""

    def __init__(self):
        self.tech_agent = TechnicalAgent()
        self.policy_agent = PolicyAgent()

        # 통계 수집
        self.stats = {
            "total": 0,
            "tech_only": 0,
            "policy_only": 0,
            "both": 0
        }

    def analyze_inquiry_type(self, inquiry):
        """문의 유형 분석"""
        tech_keywords = ["작동", "고장", "오류", "에러", "멈춤", "느림",
                        "안됨", "문제", "버그", "화면"]
        policy_keywords = ["환불", "교환", "보증", "정책", "규정",
                         "반품", "취소", "위약금"]

        needs_tech = any(word in inquiry for word in tech_keywords)
        needs_policy = any(word in inquiry for word in policy_keywords)

        return {
            "technical_needed": needs_tech,
            "policy_needed": needs_policy,
            "complexity": "both" if (needs_tech and needs_policy) else
                         ("tech" if needs_tech else
                         ("policy" if needs_policy else "unknown"))
        }

    def process(self, inquiry):
        """스마트 처리"""  # ❶
        self.stats["total"] += 1
        
        routing = self.analyze_inquiry_type(inquiry)
        
        print(f"\n{'='*60}")
        print(f"문의: {inquiry}")
        print(f"라우팅 결정: {routing}")
        print(f"{'='*60}\n")
        
        results = {}
        
        # 필요한 에이전트만 실행
        if routing["technical_needed"]:  # ❷
            print(" 기술 에이전트 활성화...")
            results["tech"] = self.tech_agent.analyze(inquiry)
            if not routing["policy_needed"]:
                self.stats["tech_only"] += 1
        
        if routing["policy_needed"]:
            print(" 정책 에이전트 활성화...")
            context = results.get("tech", {})
            results["policy"] = self.policy_agent.check(context)
            if not routing["technical_needed"]:
                self.stats["policy_only"] += 1
        
        if routing["technical_needed"] and routing["policy_needed"]:
            self.stats["both"] += 1
        
        # 결과가 없으면 기본 응답
        if not results:  # ❸
            return self._handle_unknown(inquiry)
        
        # 결과 통합
        return self._integrate_results(results)
    
    def _handle_unknown(self, inquiry):
        """알 수 없는 문의 처리"""
        return """죄송합니다. 문의 내용을 정확히 파악하지 못했습니다.

다음과 같이 구체적으로 설명해주시면 더 정확한 답변을 드릴 수 있습니다:
- 제품명과 모델명
- 발생한 문제의 구체적인 증상
- 원하시는 해결 방안 (수리/교환/환불 등)

또는 고객센터(1234-5678)로 직접 문의해주세요."""
    
    def _integrate_results(self, results):
        """결과 통합"""  # ❹
        response = "고객님께 답변드립니다.\n\n"
        
        if "tech" in results:
            response += f"【기술 진단】\n{results['tech']['analysis']}\n\n"
        
        if "policy" in results:
            response += f"【정책 안내】\n{results['policy']['guidance']}\n\n"
        
        response += "추가 문의사항이 있으시면 언제든 연락 주세요."
        return response