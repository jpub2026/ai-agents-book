import hashlib
from typing import Optional, Any
from datetime import datetime

def get(self, key: str) -> Optional[Any]:
    """캐시에서 값을 조회하고 통계를 업데이트합니다."""
    hashed_key = self._hash_key(key)
    
    if hashed_key in self.l1_cache:
        entry = self.l1_cache[hashed_key]
        if entry['expires'] > datetime.now():
            self.stats["l1_hits"] += 1
            return entry['value']
        else:
            del self.l1_cache[hashed_key]
    
    if hashed_key in self.l2_cache:
        entry = self.l2_cache[hashed_key]
        if entry['expires'] > datetime.now():
            self.stats["l2_hits"] += 1
            self._promote_to_l1(hashed_key, entry['value'])
            return entry['value']
        else:
            del self.l2_cache[hashed_key]
    
    self.stats["misses"] += 1
    return None

def _hash_key(self, key: str) -> str:
    """키를 MD5 해시로 변환합니다."""
    return hashlib.md5(key.encode()).hexdigest()
