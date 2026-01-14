def _analyze_search_need(self, query: str) -> bool:
    """검색 필요성을 빠르게 판단합니다."""
    search_triggers = ["최신", "데이터", "통계", "언제", "근거"]
    return any(trigger in query for trigger in search_triggers)

def _estimate_response_length(self, query: str) -> str:
    """응답 길이를 예측합니다."""
    if "요약" in query or "간단히" in query:
        return "short"
    elif "자세히" in query or "설명" in query:
        return "long"
    return "medium"

def _detect_language_fast(self, query: str) -> str:
    """유니코드 범위로 언어를 빠르게 감지합니다."""
    if any('\u3040' <= char <= '\u309f' for char in query):
        return "ja"
    elif any('\uac00' <= char <= '\ud7af' for char in query):
        return "ko"
    return "en"

def _assess_complexity(self, query: str) -> str:
    """쿼리 복잡도를 단어 수로 평가합니다."""
    word_count = len(query.split())
    if word_count < 10:
        return "simple"
    elif word_count < 30:
        return "moderate"
    return "complex"

def _get_cache_key(self, operation: str, query: str) -> str:
    """캐시 키를 생성합니다."""
    import hashlib
    combined = f"{operation}:{query}"
    return hashlib.md5(combined.encode()).hexdigest()
