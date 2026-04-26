import sqlite3
from pathlib import Path
from typing import Dict, Any

def get_statistics(self) -> Dict[str, Any]:
    """오프라인 저장소의 통계를 반환합니다."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM response_cache")
    cache_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM documents")
    doc_count = cursor.fetchone()[0]

    db_size = Path(self.db_path).stat().st_size / (1024**2)
    
    conn.close()
    
    return {
        "cached_responses": cache_count,
        "stored_documents": doc_count,
        "database_size_mb": round(db_size, 2),
        "cache_directory": str(self.cache_dir)
    }
