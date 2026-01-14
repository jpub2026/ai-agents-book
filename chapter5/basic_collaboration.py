"""
기본 멀티 에이전트: 두 전문가의 순차적 협업
"""

import sys
from pathlib import Path

# 4장에서 만든 LLM 브리지 재사용
# GitHub 리포지토리를 클론한 후 실행하면 정상 작동합니다
# 리포지토리 구조: ai-agents-book/chapter4/step2_real_llm/cached_llm_bridge.py
# 또는 독립 실행을 위해 CachedLLMBridge 클래스를 이 파일에 포함할 수도 있습니다
sys.path.append(str(Path(__file__).parent.parent / 'chapter4'))
from step2_real_llm.cached_llm_bridge import CachedLLMBridge

class TechnicalAgent:
    def __init__(self):
        self.llm = CachedLLMBridge(provider="mock")

    def analyze(self, problem):  # ❶
        prompt = f"""당신은 기술 지원 전문가입니다.
고객 문제: {problem}

분석하세요:
- 문제 유형: (하드웨어/소프트웨어)
- 심각도: (높음/중간/낮음)
- 권장 조치: (교체 필요/수리 가능/업데이트)"""

        response = self.llm._call(prompt)
        return {
            "analysis": response,
            "needs_replacement": "교체" in response or "하드웨어" in response
        }

class PolicyAgent:
    def __init__(self):
        self.llm = CachedLLMBridge(provider="mock")

    def check(self, tech_result):  # ❷
        prompt = f"""당신은 회사 정책 전문가입니다.
기술팀 분석: {tech_result['analysis']}
교체 필요: {tech_result['needs_replacement']}

안내하세요:
- 교환/환불 가능 여부
- 필요 절차와 서류
- 예상 처리 기간"""

        return {"guidance": self.llm._call(prompt)}

class SimpleCoordinator:
    def __init__(self):
        self.tech = TechnicalAgent()
        self.policy = PolicyAgent()

    def process(self, inquiry):  # ❸
        tech_result = self.tech.analyze(inquiry)
        policy_result = self.policy.check(tech_result)

        return f"""고객님, 문의 주신 내용을 확인했습니다.

【기술 진단】
{tech_result['analysis']}

【적용 정책】
{policy_result['guidance']}"""

if __name__ == "__main__":
    coordinator = SimpleCoordinator()
    result = coordinator.process("제품이 작동하지 않는데, 교환이나 환불이 가능한가요?")
    print(result)
