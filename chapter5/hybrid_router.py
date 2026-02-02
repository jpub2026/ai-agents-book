"""
하이브리드 라우팅 1단계: 키워드 우선, 불명확시 LLM 사용
목표: 속도와 정확도의 균형
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from smart_coordinator import SmartCoordinator

# 상위 디렉토리의 llm_bridge 사용
sys.path.append(str(Path(__file__).parent.parent))
from llm_bridge import CachedLLMBridge


# 하이브리드 라우팅: 키워드 우선 전략
class HybridCoordinator(SmartCoordinator):
    def __init__(self):
        super().__init__()
        self.routing_llm = CachedLLMBridge(provider="openai")

        # 라우팅 통계
        self.routing_stats = {
            "keyword": 0,
            "llm": 0
        }

    def analyze_inquiry_type_hybrid(self, inquiry):  
        """하이브리드 라우팅: 키워드 우선, 불명확시 LLM 사용"""

        # 1단계: 빠른 키워드 매칭
        tech_keywords = ["작동", "고장", "오류", "에러", "멈춤"]
        policy_keywords = ["환불", "교환", "보증", "반품"]

        has_tech = any(word in inquiry for word in tech_keywords)
        has_policy = any(word in inquiry for word in policy_keywords)

        # 명확한 케이스는 즉시 반환  
        if has_policy and not has_tech:
            self.routing_stats["keyword"] += 1
            return {
                "technical_needed": False,
                "policy_needed": True,
                "complexity": "policy",
                "method": "keyword"
            }

        if has_tech and not has_policy:
            self.routing_stats["keyword"] += 1
            return {
                "technical_needed": True,
                "policy_needed": False,
                "complexity": "tech",
                "method": "keyword"
            }

        # 2단계: 애매한 경우만 LLM에 물어본다.  
        self.routing_stats["llm"] += 1

        prompt = f"""다음 고객 문의를 분류하세요.

문의: {inquiry}

다음 중 하나로 답변하세요:
- TECH: 기술적 문제(작동, 고장, 오류 등)
- POLICY: 정책 문의(환불, 교환, 보증 등)
- BOTH: 기술과 정책 모두 필요
- UNKNOWN: 판단 불가

답변 형식: 분류결과만 한 단어로"""

        llm_result = self.routing_llm._call(prompt)
        return self._parse_llm_result(llm_result)

    #하이브리드 라우팅: LLM 응답 파싱 및 통계
    """
    하이브리드 라우팅 2단계: LLM 응답 파싱 및 통계 수집
    목표: 안전한 응답 처리와 성능 측정
    """

    def _parse_llm_result(self, result): 
        """LLM 응답을 라우팅 정보로 변환"""
        result_upper = result.strip().upper()

        if "TECH" in result_upper and "POLICY" not in result_upper:
            return {
                "technical_needed": True,
                "policy_needed": False,
                "complexity": "tech",
                "method": "llm"
            }
        elif "POLICY" in result_upper and "TECH" not in result_upper:
            return {
                "technical_needed": False,
                "policy_needed": True,
                "complexity": "policy",
                "method": "llm"
            }
        elif "BOTH" in result_upper:
            return {
                "technical_needed": True,
                "policy_needed": True,
                "complexity": "both",
                "method": "llm"
            }
        else:  
            return {
                "technical_needed": False,
                "policy_needed": False,
                "complexity": "unknown",
                "method": "llm"
            }

    def print_routing_stats(self):  
        """라우팅 방법 통계 출력"""
        total = self.routing_stats["keyword"] + self.routing_stats["llm"]
        if total == 0:
            return

        print(f"\n{'='*60}")
        print("라우팅 방법 통계")
        print(f"{'='*60}")
        print(f"키워드 매칭: {self.routing_stats['keyword']}건 "
              f"({self.routing_stats['keyword']/total*100:.1f}%)")
        print(f"LLM 분류: {self.routing_stats['llm']}건 "
              f"({self.routing_stats['llm']/total*100:.1f}%)")


# 테스트
if __name__ == "__main__":
    coordinator = HybridCoordinator()

    test_cases = [
        "환불 받고 싶어요",  # keyword: policy
        "제품이 자꾸 멈춰요",  # keyword: tech
        "고장났는데 교환 가능한가요?",  # keyword: both -> LLM
        "영업시간이 언제인가요?",  # keyword: none -> LLM
    ]

    for inquiry in test_cases:
        print(f"\n문의: {inquiry}")
        routing = coordinator.analyze_inquiry_type_hybrid(inquiry)
        print(f"라우팅 결과: {routing}")

    coordinator.print_routing_stats()
