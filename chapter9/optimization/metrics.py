import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass
import time

@dataclass
class PerformanceMetrics:
    """각 작업의 성능을 측정하는 메트릭입니다."""
    operation: str
    start_time: float
    end_time: float
    tokens_used: int = 0
    cache_hit: bool = False
    
    @property
    def latency_ms(self) -> int:
        """작업의 지연 시간을 밀리초로 반환합니다."""
        return int((self.end_time - self.start_time) * 1000)
