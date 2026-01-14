from typing import List, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from indexing import Document

async def retrieve(
    self, 
    query: str, 
    top_k: int = 3,
    threshold: float = 0.3
) -> List[Tuple[Document, float]]:
    """쿼리와 관련된 문서를 검색합니다."""
    if not self.documents:
        return []
        
    query_embedding = self.vectorizer.transform([query])
    
    similarities = cosine_similarity(
        query_embedding, 
        self.embeddings
    )[0]
    
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        score = similarities[idx]
        if score >= threshold:
            results.append((
                self.documents[idx],
                float(score)
            ))
            
    return results
