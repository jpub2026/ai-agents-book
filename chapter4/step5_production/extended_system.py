"""
확장된 FAQ 클래스
모든 확장 모듈을 통합한 메인 클래스
"""
import sys
import time
from pathlib import Path

# 이전 단계 모듈
sys.path.append(str(Path(__file__).parent.parent))
from step4_agent.memory_agent import MemoryReActAgent

# 확장 모듈들 (같은 디렉토리에서 불러오기)
from .statistics import StatisticsTracker
from .metrics import MetricsCollector
from .analyzer import Analyzer
from .session import SessionManager

class ExtendedFAQSystem(MemoryReActAgent):
    def __init__(self):
        super().__init__()
        
        # 4개 확장 모듈 초기화
        self.stats = StatisticsTracker()
        self.metrics = MetricsCollector()
        self.analyzer = Analyzer()
        self.session = SessionManager()
    
    def query(self, message: str) -> dict:
        """모니터링이 추가된 쿼리 처리"""
        start = time.time()
        
        try:
            response = self.chat(message)
            elapsed = time.time() - start
            
            # 성공 기록
            self.stats.record(True, elapsed)
            self.metrics.add(message, elapsed, True)
            
            return {"success": True, "response": response}
            
        except Exception as e:
            self.stats.record(False)
            return {"success": False, "error": str(e)}
    
    def get_dashboard(self) -> dict:
        """관리자용 대시보드 데이터"""
        return {
            "stats": self.stats.get_summary(),
            "recent": self.metrics.get_recent(),
            "p95": self.analyzer.calculate_p95(
                self.stats.stats["response_times"]
            )
        }
