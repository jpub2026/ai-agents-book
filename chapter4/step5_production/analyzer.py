"""
성능 분석 도구
수집된 데이터를 분석하여 인사이트를 제공합니다
"""
from typing import List, Dict

class Analyzer:
    @staticmethod
    def calculate_p95(times: List[float]) -> float:
        """P95 응답 시간 계산"""
        if not times:
            return 0
        
        sorted_times = sorted(times)
        index = int(len(sorted_times) * 0.95)
        return sorted_times[min(index, len(sorted_times) - 1)]
    
    @staticmethod
    def find_slow_queries(metrics: List[Dict], 
                         threshold: float = 2.0) -> List[Dict]:
        """느린 쿼리 식별"""
        slow = []
        for m in metrics:
            if m.get("time", 0) > threshold:
                slow.append({
                    "query": m["query"],
                    "time": m["time"]
                })
        
        return sorted(slow, key=lambda x: x["time"], reverse=True)
