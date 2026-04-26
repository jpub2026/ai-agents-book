from typing import List
from dataclasses import dataclass

@dataclass
class RAGPipeline:
    """RAG 파이프라인 기본 클래스"""
    documents: List = None

    async def retrieve(self, query: str, top_k: int = 3):
        return []

class RAGAgent:
    """문서 검색을 활용하는 증강 에이전트입니다."""
    
    def __init__(
        self, 
        rag_pipeline: RAGPipeline,
        mcp_client,
        use_citations: bool = True
    ):
        self.rag = rag_pipeline
        self.mcp_client = mcp_client
        self.use_citations = use_citations
