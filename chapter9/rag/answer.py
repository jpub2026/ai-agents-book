from typing import Optional

async def answer(
    self, 
    query: str,
    use_rag: Optional[bool] = None
) -> dict:
    """RAG를 활용하여 답변을 생성합니다."""
    
    if use_rag is None:
        use_rag = self._should_use_rag(query)
        
    context = ""
    sources = []
    
    if use_rag:
        retrieved = await self.rag.retrieve(query, top_k=3)

        if retrieved:
            context_parts = []
            for doc, score in retrieved:
                context_parts.append(
                    f"[출처: {doc.title}]\n{doc.content}"
                )
                sources.append({
                    "id": doc.id,
                    "title": doc.title,
                    "score": round(score, 3)
                })
                
            context = "\n\n".join(context_parts)
    
    prompt = self._build_augmented_prompt(
        query, 
        context, 
        self.use_citations
    )
    
    result = await self.mcp_client.call_tool(
        "generate_response",
        {
            "prompt": prompt,
            "max_tokens": 500
        }
    )
    
    response = result.get("response", "")
    
    if self.use_citations and sources:
        response = self._add_citations(response, sources)
        
    return {
        "query": query,
        "response": response,
        "sources": sources,
        "used_rag": use_rag,
        "metadata": {
            "latency_ms": result.get("latency_ms", 0),
            "tokens_used": result.get("tokens", 0)
        }
    }
