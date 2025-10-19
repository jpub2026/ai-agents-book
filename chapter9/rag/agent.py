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
