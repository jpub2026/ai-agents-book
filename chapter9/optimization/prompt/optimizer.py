class PromptOptimizer:
    """프롬프트를 압축하고 최적화하는 도구입니다."""
    
    def __init__(
        self,
        max_length: int = 2000,
        compression_ratio: float = 0.7
    ):
        self.max_length = max_length
        self.compression_ratio = compression_ratio
        
    def optimize(
        self,
        prompt: str,
        priority: str = "balanced"
    ) -> str:
        """우선순위에 따라 프롬프트를 최적화합니다."""
        
        prompt = self._remove_duplicates(prompt)
        prompt = self._clean_whitespace(prompt)
        
        if len(prompt) > self.max_length:
            if priority == "context":
                prompt = self._compress_keeping_context(prompt)
            elif priority == "instruction":
                prompt = self._compress_keeping_instruction(prompt)
            else:
                prompt = self._balanced_compression(prompt)

        prompt = self._restructure(prompt)

        return prompt
