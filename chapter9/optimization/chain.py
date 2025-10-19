class OptimizedChain:
    """성능 최적화된 처리 체인입니다."""
    
    def __init__(self, cache_enabled: bool = True):
        self.cache_enabled = cache_enabled
        self.cache = {}
        self.metrics = []
        
    async def plan(
        self, 
        query: str
    ) -> Dict[str, Any]:
        """쿼리 처리 전략을 빠르게 수립합니다."""
        start = time.time()
        
        cache_key = self._get_cache_key("plan", query)
        if self.cache_enabled and cache_key in self.cache:
            self.metrics.append(
                PerformanceMetrics(
                    "plan", 
                    start, 
                    time.time(),
                    cache_hit=True
                )
            ) 
            return self.cache[cache_key]
        
        plan = {
            "needs_search": self._analyze_search_need(query),
            "expected_length": self._estimate_response_length(query),
            "language": self._detect_language_fast(query),
            "complexity": self._assess_complexity(query)
        }
        
        if self.cache_enabled:
            self.cache[cache_key] = plan
            
        self.metrics.append(
            PerformanceMetrics("plan", start, time.time())
        )
        
        return plan
