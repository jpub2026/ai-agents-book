"""
메트릭 수집 시스템
각 쿼리의 상세 정보를 기록합니다
"""
from datetime import datetime
from typing import List, Dict

class MetricsCollector:
    def __init__(self, max_size: int = 100):
        self.metrics = []
        self.max_size = max_size
    
    def add(self, query: str, response_time: float, success: bool):
        """메트릭 추가 (메모리 관리 포함)"""
        metric = {
            "timestamp": datetime.now(),
            "query": query[:50],  #처음 50자만 저장
            "time": response_time,
            "success": success
        }
        
        self.metrics.append(metric)
        
        # 오래된 데이터 자동 삭제
        if len(self.metrics) > self.max_size:
            self.metrics.pop(0)
    
    def get_recent(self, n: int = 5) -> List[Dict]:
        """최근 n개 메트릭 반환"""
        return self.metrics[-n:]
