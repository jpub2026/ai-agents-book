"""
확장된 FAQ 클래스
모든 확장 모듈을 통합한 메인 클래스
"""
import sys
import time
from pathlib import Path

# 이전 단계 모듈을 불러오기 위해 __file__ 기준으로 경로를 추가합니다.
_CH4_DIR = Path(__file__).resolve().parent.parent
_PROD_DIR = Path(__file__).resolve().parent
for _p in (_CH4_DIR, _PROD_DIR):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from step4_agent.memory_agent import MemoryReActAgent

# 같은 디렉터리의 모듈들 (python extended_system.py 로 직접 실행되는 경우
# 상대 import 가 깨지므로 절대 import 로 불러옵니다).
from statistics import StatisticsTracker
from metrics import MetricsCollector
from analyzer import Analyzer
from session import SessionManager


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
            ),
        }


if __name__ == "__main__":
    system = ExtendedFAQSystem()
    print(system.query("환불 정책이 어떻게 되나요?"))
    print(system.get_dashboard())
