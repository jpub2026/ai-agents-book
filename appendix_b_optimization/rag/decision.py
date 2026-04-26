from typing import List

def _should_use_rag(self, query: str) -> bool:
    """쿼리를 분석하여 RAG 사용 여부를 판단합니다."""
    rag_keywords = [
        "최신", "정보", "데이터", "통계", 
        "언제", "얼마나", "몇", "근거"
    ]
    
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in rag_keywords)

def _build_augmented_prompt(
    self, 
    query: str, 
    context: str,
    use_citations: bool
) -> str:
    """검색 결과가 포함된 프롬프트를 생성합니다."""
    prompt_parts = []
    
    if context:
        prompt_parts.append("다음 컨텍스트를 참고하여 답변하세요:")
        prompt_parts.append(context)
        prompt_parts.append("")
        
    prompt_parts.append(f"질문: {query}")
    
    if use_citations:
        prompt_parts.append(
            "\n답변 시 출처를 [1], [2] 형식으로 표시하세요."
        )
        
    return "\n".join(prompt_parts)

def _add_citations(
    self, 
    response: str, 
    sources: List[dict]
) -> str:
    """응답에 출처를 각주 형식으로 추가합니다."""
    citations = [
        f"[{i+1}] {source['title']} (신뢰도: {source['score']})"
        for i, source in enumerate(sources)
    ]
    
    if citations:
        response += "\n\n참고 자료:\n" + "\n".join(citations)
        
    return response
