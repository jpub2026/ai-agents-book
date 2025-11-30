import sqlite3
import pickle
from typing import Optional, List, Dict, Any
import numpy as np

def store_document(
    self,
    doc_id: str,
    title: str,
    content: str,
    embedding: Optional[np.ndarray] = None
):
    """문서를 로컬 데이터베이스에 저장합니다."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    embedding_blob = None
    if embedding is not None:
        embedding_blob = pickle.dumps(embedding)
        
    cursor.execute("""
        INSERT OR REPLACE INTO documents 
        (id, title, content, embedding)
        VALUES (?, ?, ?, ?)
    """, (doc_id, title, content, embedding_blob))

    conn.commit()
    conn.close()
    
def search_offline(
    self,
    query: str,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """오프라인 상태에서 문서를 검색합니다."""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title, content 
        FROM documents 
        WHERE content LIKE ? OR title LIKE ?
        LIMIT ?
    """, (f"%{query}%", f"%{query}%", limit))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            "id": row[0],
            "title": row[1],
            "content": row[2][:200]
        })
        
    conn.close()
    return results
