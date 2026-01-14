import sqlite3
import json
from typing import Optional

def cache_response(
    self,
    query: str,
    response: str,
    metadata: dict = None
):
    """생성된 응답을 로컬에 캐싱합니다."""
    import hashlib
    
    query_hash = hashlib.sha256(query.encode()).hexdigest()
    
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO response_cache 
        (query_hash, query, response, metadata)
        VALUES (?, ?, ?, ?)
    """, (
        query_hash,
        query,
        response,
        json.dumps(metadata) if metadata else "{}"
    ))
    
    conn.commit()
    conn.close()
    
def get_cached_response(self, query: str) -> Optional[str]:
    """캐시된 응답을 조회합니다."""
    import hashlib
    
    query_hash = hashlib.sha256(query.encode()).hexdigest()
    
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT response, metadata 
        FROM response_cache 
        WHERE query_hash = ?
    """, (query_hash,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "response": result[0],
            "metadata": json.loads(result[1]),
            "cached": True
        }
    return None
