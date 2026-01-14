import time
from typing import Any, Dict


def generate(
    self,
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 500,
    top_p: float = 0.9,
    top_k: int = 40,
    repeat_penalty: float = 1.1
) -> Dict[str, Any]:
    """로컬 LLM으로 텍스트를 생성합니다."""
    if self.model is None:
        raise RuntimeError("모델이 로드되지 않았습니다.")
    
    start_time = time.time()
    
    try:
        output = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            repeat_penalty=repeat_penalty,
            echo=False
        )
        
        generation_time = time.time() - start_time
        
        # 결과 파싱
        text = output['choices'][0]['text']

        return {
            "text": text,
            "metrics": {
                "latency_ms": int(generation_time * 1000),
                "tokens_generated": output['usage']['completion_tokens'],
                "tokens_per_second": output['usage']['completion_tokens'] / generation_time,
                "model": self.model_path.name,
                "local": True
            }
        }
        
    except Exception as e:
        print(f"생성 실패: {e}")
        raise

def generate_stream(
    self,
    prompt: str,
    **kwargs
):
    """스트리밍 방식으로 텍스트를 생성합니다."""
    if self.model is None:
        raise RuntimeError("모델이 로드되지 않았습니다.")
    
    stream = self.model(
        prompt,
        max_tokens=kwargs.get('max_tokens', 500),
        temperature=kwargs.get('temperature', 0.7),
        stream=True
    )
    
    for output in stream:
        token = output['choices'][0]['text']
        yield token
        
def get_model_info(self) -> Dict[str, Any]:
    """현재 모델의 상세 정보를 반환합니다."""
    if self.model is None:
        return {}
    
    return {
        "model_path": str(self.model_path),
        "model_name": self.model_path.name,
        "context_size": self.n_ctx,
        "gpu_layers": self.n_gpu_layers,
        "threads": self.n_threads or "auto",
        "file_size_mb": self.model_path.stat().st_size / (1024**2)
    }
