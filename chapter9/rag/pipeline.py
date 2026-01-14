from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGPipeline:
    """문서 검색과 임베딩을 관리하는 RAG 파이프라인입니다."""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2)
        )
        self.documents = []
        self.embeddings = None
