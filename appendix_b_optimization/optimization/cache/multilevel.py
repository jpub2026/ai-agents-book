import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional, Any

class MultiLevelCache:
    """L1과 L2 두 계층의 캐싱 시스템입니다."""
    
    def __init__(
        self,
        l1_ttl_seconds: int = 60, 
        l2_ttl_seconds: int = 3600,
        max_l1_size: int = 100,
        max_l2_size: int = 1000
    ):
        self.l1_cache = {}
        self.l2_cache = {}
        self.l1_ttl = timedelta(seconds=l1_ttl_seconds)
        self.l2_ttl = timedelta(seconds=l2_ttl_seconds)
        self.max_l1_size = max_l1_size
        self.max_l2_size = max_l2_size
        self.stats = {
            "l1_hits": 0,
            "l2_hits": 0,
            "misses": 0
        }
