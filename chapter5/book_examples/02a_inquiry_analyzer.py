"""
조건부 협업 1단계: 문의 유형 분석
목표: 어떤 전문가가 필요한지 판단
"""
from typing import Dict, Any

# 01_basic_collaboration에서 에이전트 클래스들 재사용
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

# 파일 이름에 숫자가 있어서 직접 import가 어려우므로 importlib 사용
import importlib.util
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
        """문의 유형 분석"""  # ❶
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