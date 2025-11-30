"""
하이브리드 시스템 2단계: 적응형 라우터
목표: 복잡도에 따라 최적 시스템 선택
"""
import sys
from pathlib import Path
import time
from typing import Dict
import importlib.util

# 필요한 모듈들 가져오기
# 02b_conditional_execution에서 SmartCoordinator 가져오기
spec_smart = importlib.util.spec_from_file_location(
    "conditional_execution",
    Path(__file__).parent / "02b_conditional_execution.py"
)
cond_exec = importlib.util.module_from_spec(spec_smart)
spec_smart.loader.exec_module(cond_exec)
SmartCoordinator = cond_exec.SmartCoordinator

# 03c_langgraph_run에서 LangGraphWorkflow 가져오기
spec_langgraph = importlib.util.spec_from_file_location(
    "langgraph_run",
    Path(__file__).parent / "03c_langgraph_run.py"
)
langgraph_run = importlib.util.module_from_spec(spec_langgraph)
spec_langgraph.loader.exec_module(langgraph_run)
LangGraphWorkflow = langgraph_run.LangGraphWorkflow

# 05a_complexity_analyzer에서 ComplexityAnalyzer 가져오기
spec_analyzer = importlib.util.spec_from_file_location(
    "complexity_analyzer",
    Path(__file__).parent / "05a_complexity_analyzer.py"
)
complexity_analyzer = importlib.util.module_from_spec(spec_analyzer)
spec_analyzer.loader.exec_module(complexity_analyzer)
ComplexityAnalyzer = complexity_analyzer.ComplexityAnalyzer


class HybridSystem:
    """복잡도 기반 적응형 멀티 에이전트 시스템"""
    
    def __init__(self):
        # 세 가지 처리 시스템
        self.simple_coordinator = SmartCoordinator()  # 직접 구현
        self.langgraph_workflow = LangGraphWorkflow()  # LangGraph
        
        # CrewAI 설정 (실제 환경에서 사용 시 코드 5-4a의 주석 해제 후 아래 주석 해제)
        # self.crewai_team = CrewAITeam()
        
        self.analyzer = ComplexityAnalyzer()
        
        # 통계 수집
        self.stats = {
            "total": 0,
            "simple": 0,
            "moderate": 0,
            "complex": 0,
            "total_time": 0,
            "avg_time_by_complexity": {}
        }
    
    def route(self, inquiry: str) -> Dict:
        """적절한 시스템으로 라우팅"""  # ❶
        start_time = time.time()
        self.stats["total"] += 1
        
        # 복잡도 분석
        analysis = self.analyzer.analyze(inquiry)
        complexity = analysis["complexity"]
        
        print(f"\n{'='*60}")
        print(f"문의: {inquiry}")
        print(f"{'='*60}")
        print(f"복잡도 분석:")
        print(f"  - 분류: {complexity}")
        print(f"  - 점수: {analysis['score']:.1f}/10")
        print(f"  - 이유: {analysis['reason']}")
        print(f"{'='*60}\n")
        
        # 시스템 선택 및 실행
        if complexity == "simple":  # ❷
            print("선택된 시스템: 직접 구현 (빠른 처리)")
            result = self.simple_coordinator.process(inquiry)
            system_used = "direct"
        elif complexity == "moderate":
            print("선택된 시스템: LangGraph (구조화된 워크플로우)")
            result = self.langgraph_workflow.process(inquiry)
            system_used = "langgraph"
        else:  # complex
            print("선택된 시스템: CrewAI (전문가 팀 협업)")
            # 실제로는 self.crewai_team.process(inquiry)
            result = "복잡한 문의는 전문가 팀이 처리합니다. (데모)"
            system_used = "crewai"
        
        # 통계 업데이트
        processing_time = time.time() - start_time
        self._update_stats(complexity, processing_time)
        
        return {
            "inquiry": inquiry,
            "complexity_analysis": analysis,
            "system_used": system_used,
            "result": result,
            "processing_time": processing_time
        }
    
    def _update_stats(self, complexity: str, duration: float):
        """통계 업데이트"""  # ❸
        self.stats[complexity] += 1
        self.stats["total_time"] += duration
        
        # 복잡도별 평균 시간 계산
        count = self.stats[complexity]
        current_avg = self.stats["avg_time_by_complexity"].get(complexity, 0)
        new_avg = ((current_avg * (count - 1)) + duration) / count
        self.stats["avg_time_by_complexity"][complexity] = new_avg