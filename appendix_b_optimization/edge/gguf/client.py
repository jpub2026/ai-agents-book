"""GGUF 로컬 LLM 클라이언트
설치 필요: pip install llama-cpp-python  (빌드 시간이 오래 걸릴 수 있음)
"""
import time
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from llama_cpp import Llama
except ImportError as e:
    raise ImportError(
        "llama-cpp-python 패키지가 필요합니다. 설치: pip install llama-cpp-python"
    ) from e

class GGUFLocalLLM:
    """GGUF 형식의 모델을 로컬에서 실행합니다."""
    
    def __init__(
        self,
        model_path: str,
        n_ctx: int = 2048,
        n_gpu_layers: int = 0,
        n_threads: Optional[int] = None
    ):
        self.model_path = Path(model_path)
        self.n_ctx = n_ctx
        self.n_gpu_layers = n_gpu_layers
        self.n_threads = n_threads
        self.model = None

        self._load_model()
