"""
하이브리드 검색 FAQ 도구
실제 sentence-transformers를 사용한 의미 검색 구현
"""

from typing import List, Dict, Tuple, Type, Optional, Any
from dataclasses import dataclass
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class FAQSearchInput(BaseModel):
    """FAQ 검색 입력 스키마"""
    query: str = Field(description="검색할 질문 또는 키워드")

@dataclass
class FAQItem:
    """FAQ 항목"""
    question: str
    answer: str
    keywords: List[str]

class HybridFAQTool(BaseTool):
    """하이브리드 검색을 사용하는 FAQ 도구"""
    
    name: str = "hybrid_faq_search"
    description: str = """FAQ 검색 도구입니다. 
    키워드와 의미를 모두 이해하여 최적의 답변을 제공합니다."""
    args_schema: Type[BaseModel] = FAQSearchInput
    
    def __init__(self):
        super().__init__()
        
        # 임베딩 모델 로드 (처음 실행 시 다운로드)
        self.encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # ❶
        
        # FAQ 데이터 준비
        self.faqs = [
            FAQItem(
                question="환불 정책이 어떻게 되나요?",
                answer="구매일로부터 14일 이내에 환불 가능합니다.",
                keywords=["환불", "반품", "리펀드", "취소", "되돌리다"]
            ),
            FAQItem(
                question="배송은 얼마나 걸리나요?",
                answer="표준 배송은 3-5 영업일이 소요됩니다.",
                keywords=["배송", "택배", "배달", "도착"]
            )
        ]
        
        # 검색 인덱스 생성
        self._create_indices()
    
    def _create_indices(self):
        """검색을 위한 인덱스 생성"""
        # 의미 검색용: FAQ를 벡터로 변환
        texts = [f"{faq.question} {' '.join(faq.keywords)}" for faq in self.faqs]
        self.faq_embeddings = self.encoder.encode(texts)
        
        # 키워드 검색용: BM25 인덱스
        tokenized_docs = [text.lower().split() for text in texts]
        self.bm25 = BM25Okapi(tokenized_docs)
    
    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """하이브리드 검색 실행"""
        
        # 1. 의미 검색: 쿼리를 벡터로 변환하고 유사도 계산
        query_embedding = self.encoder.encode([query])[0]
        semantic_scores = np.dot(self.faq_embeddings, query_embedding)
        semantic_scores = (semantic_scores + 1) / 2  # 0~1로 정규화
        
        # 2. 키워드 검색: BM25 점수 계산
        query_tokens = query.lower().split()
        keyword_scores = self.bm25.get_scores(query_tokens)
        if keyword_scores.max() > 0:
            keyword_scores = keyword_scores / keyword_scores.max()  # 정규화
        
        # 3. 점수 융합 (의미 60%, 키워드 40%)
        final_scores = 0.6 * semantic_scores + 0.4 * keyword_scores
        
        # 최고 점수 FAQ 선택
        best_idx = np.argmax(final_scores)
        if final_scores[best_idx] < 0.2:  # 최소 신뢰도
            return "관련 정보를 찾을 수 없습니다."
        
        faq = self.faqs[best_idx]
        return f"Q: {faq.question}\nA: {faq.answer}\n(신뢰도: {final_scores[best_idx]:.0%})"
    
    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        return self._run(query)
