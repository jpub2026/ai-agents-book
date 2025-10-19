from llama_cpp import Llama
from pathlib import Path
from typing import Optional, Dict, Any
import time

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
