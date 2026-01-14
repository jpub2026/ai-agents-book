"""
하이브리드 시스템: 복잡도 분석기
목표: 문의 복잡도를 정확히 측정
"""

from typing import Dict


# [코드 5-6] 복잡도 분석기
class ComplexityAnalyzer:
    """문의 복잡도를 분석하는 전문 모듈"""

    def analyze(self, inquiry: str) -> Dict:
        """문의 복잡도 분석"""
        # 여러 지표로 복잡도 측정
        word_count = len(inquiry.split())
        question_marks = inquiry.count('?')

        tech_keywords = ["작동", "고장", "오류", "에러", "멈춤", "느림"]
        policy_keywords = ["환불", "교환", "보증", "정책"]
        product_keywords = ["추천", "업그레이드", "다른", "대체"]

        topic_count = sum([
            any(k in inquiry for k in tech_keywords),
            any(k in inquiry for k in policy_keywords),
            any(k in inquiry for k in product_keywords)
        ])

        # 복잡도 점수 계산 (0-10) ❶
        complexity_score = (
            min(word_count / 10, 3) +  # 단어 수 (최대 3점)
            min(question_marks * 2, 2) +  # 질문 개수 (최대 2점)
            topic_count * 2  # 주제 개수 (최대 6점)
        )

        # 복잡도 분류
        if complexity_score < 3:
            complexity = "simple"
            reason = "단일 주제, 짧은 문의"
        elif complexity_score < 6:
            complexity = "moderate"
            reason = "2-3개 주제, 중간 길이"
        else:
            complexity = "complex"
            reason = "다중 주제, 긴 문의, 복잡한 의사결정 필요"

        return {
            "complexity": complexity,
            "score": complexity_score,
            "reason": reason,
            "word_count": word_count,
            "topics": topic_count
        }
