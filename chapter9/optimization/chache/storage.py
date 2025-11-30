from typing import Any
from datetime import datetime

def set(
    self, 
    key: str, 
    value: Any,
    tier: str = "l1"
):
    """캐시에 값을 저장합니다."""
    hashed_key = self._hash_key(key)
    
    if tier == "l1":
        if len(self.l1_cache) >= self.max_l1_size:
            self._evict_l1()
            
        self.l1_cache[hashed_key] = {
            'value': value,
            'expires': datetime.now() + self.l1_ttl,
            'access_count': 0
        }
    else:
        if len(self.l2_cache) >= self.max_l2_size:
            self._evict_l2()
            
        self.l2_cache[hashed_key] = {
            'value': value,
            'expires': datetime.now() + self.l2_ttl,
            'access_count': 0
        }

def _promote_to_l1(self, hashed_key: str, value: Any):
    """L2 항목을 L1으로 승격합니다."""
    if len(self.l1_cache) >= self.max_l1_size:
        self._evict_l1()
        
    self.l1_cache[hashed_key] = {
        'value': value,
        'expires': datetime.now() + self.l1_ttl,
        'access_count': 0
    }

def _evict_l1(self):
    """L1 캐시에서 가장 오래된 항목을 제거합니다."""
    if self.l1_cache:
        oldest = min(
            self.l1_cache.items(),
            key=lambda x: x[1]['expires']
        )
        del self.l1_cache[oldest[0]]

def _evict_l2(self):
    """L2 캐시에서 가장 오래된 항목을 제거합니다."""
    if self.l2_cache:
        oldest = min(
            self.l2_cache.items(),
            key=lambda x: x[1]['expires']
        )
        del self.l2_cache[oldest[0]]

def get_stats(self) -> dict:
    """캐시 통계를 반환합니다."""
    total_requests = sum(self.stats.values())
    if total_requests == 0:
        hit_rate = 0
    else:
        hit_rate = (
            self.stats["l1_hits"] + self.stats["l2_hits"]
        ) / total_requests
        
    return {
        **self.stats,
        "hit_rate": round(hit_rate, 3),
        "l1_size": len(self.l1_cache),
        "l2_size": len(self.l2_cache)
    }
