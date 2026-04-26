from typing import Dict, Any
from router import LanguageRouter, LanguageConfig

# 언어별 프로세서 (예시 구현)
class KoreanProcessor:
    def preprocess(self, text): return text.strip()
    def postprocess(self, text): return text

class EnglishProcessor:
    def preprocess(self, text): return text.strip()
    def postprocess(self, text): return text

class JapaneseProcessor:
    def preprocess(self, text): return text.strip()
    def postprocess(self, text): return text

class MultilingualPipeline:
    """다국어 처리를 위한 통합 파이프라인입니다."""
    
    def __init__(self, router: LanguageRouter, mcp_client):
        self.router = router
        self.mcp_client = mcp_client
        self.processors = self._init_processors()
        
    def _init_processors(self) -> Dict[str, Any]:
        """언어별 전처리와 후처리를 담당하는 프로세서를 초기화합니다."""
        return {
            "ko": KoreanProcessor(),
            "en": EnglishProcessor(),
            "ja": JapaneseProcessor()
        }
    
    async def process(self, query: str) -> Dict[str, Any]:
        """쿼리를 받아 언어에 맞는 처리를 수행하고 응답을 생성합니다."""
        lang = self.router.detect_language(query)
        print(f"감지된 언어: {lang}")
        
        processor = self.processors.get(lang, self.processors["en"])
        preprocessed = processor.preprocess(query)
        
        prompt = self._build_prompt(lang, preprocessed)
        
        result = await self.mcp_client.call_tool(
            "generate_response",
            {"prompt": prompt, "language": lang}
        )
        
        postprocessed = processor.postprocess(result.get("response", ""))
        
        return {
            "language": lang,
            "original_query": query,
            "response": postprocessed,
            "metadata": {
                "processing_time_ms": result.get("latency_ms", 0),
                "tokens_used": result.get("tokens", 0)
            }
        }
    
    def _build_prompt(self, lang: str, query: str) -> str:
        """언어에 맞는 프롬프트를 생성합니다."""
        template = self.router.templates.get(lang)
        style = getattr(self.router.config, f"{lang}_style")
        
        return template.format(
            style=style,
            query=query
        )[:self.router.config.max_response_length]
