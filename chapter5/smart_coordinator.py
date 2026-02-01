"""
조건부 협업: 문의 유형 분석 및 스마트 처리
"""
import sys
from pathlib import Path

# basic_collaboration에서 에이전트 클래스들 재사용
sys.path.append(str(Path(__file__).parent))
from basic_collaboration import TechnicalAgent, PolicyAgent


# [코드 5-2] 조건부 협업 - 문의 유형 분석
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

    # [코드 5-3] 조건부 협업 - 실행 및 결과 통합
    def process(self, inquiry):
        """스마트 처리""" 
        self.stats["total"] += 1

        routing = self.analyze_inquiry_type(inquiry)

        print(f"\n{'='*60}")
        print(f"문의: {inquiry}")
        print(f"라우팅 결정: {routing}")
        print(f"{'='*60}\n")

        results = {}

        # 필요한 에이전트만 실행
        if routing["technical_needed"]: 
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
        if not results:  
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
        """결과 통합""" 
        response = "고객님께 답변드립니다.\n\n"

        if "tech" in results:
            response += f"【기술 진단】\n{results['tech']['analysis']}\n\n"

        if "policy" in results:
            response += f"【정책 안내】\n{results['policy']['guidance']}\n\n"

        response += "추가 문의사항이 있으시면 언제든 연락 주세요."
        return response

    # [코드 5-4] 조건부 협업 - 통계 분석
    def print_stats(self):
        """처리 통계 출력"""
        total = self.stats["total"]
        if total == 0:
            print("아직 처리된 문의가 없습니다.")
            return

        print(f"\n{'='*60}")
        print("처리 통계")
        print(f"{'='*60}")
        print(f"총 문의: {total}건")
        print(f"기술 문의만: {self.stats['tech_only']}건 "
              f"({self.stats['tech_only']/total*100:.1f}%)")
        print(f"정책 문의만: {self.stats['policy_only']}건 "
              f"({self.stats['policy_only']/total*100:.1f}%)")
        print(f"복합 문의: {self.stats['both']}건 "
              f"({self.stats['both']/total*100:.1f}%)")


# 테스트
if __name__ == "__main__":
    coordinator = SmartCoordinator()

    test_cases = [
        "제품이 자꾸 멈춰요",
        "환불 받고 싶어요",
        "고장났는데 교환 가능한가요?",
        "영업시간이 언제인가요?"
    ]

    for inquiry in test_cases:
        result = coordinator.process(inquiry)
        print(result)
        print()

    coordinator.print_stats()
