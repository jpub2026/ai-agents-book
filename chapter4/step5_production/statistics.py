"""
통계 추적 시스템
전체 시스템의 성능과 사용 패턴을 추적합니다
"""
from datetime import datetime
from typing import Dict, Any

class StatisticsTracker:
    def __init__(self):
        self.stats = {
            "total": 0,
            "success": 0,
            "response_times": [],
            "start_time": datetime.now()
        }
    
    def record(self, success: bool, time: float = None):
        """쿼리 결과 기록"""
        self.stats["total"] += 1
        if success:
            self.stats["success"] += 1
            if time:
                self.stats["response_times"].append(time)
    
    def get_summary(self) -> Dict[str, Any]:
        """통계 요약 반환"""
        total = self.stats["total"]
        if total == 0:
            return {"message": "No data"}
        
        return {
            "total": total,
            "success_rate": self.stats["success"] / total * 100,
            "avg_time": sum(self.stats["response_times"]) / 
                       len(self.stats["response_times"]) 
                       if self.stats["response_times"] else 0
        }
