import time
from typing import Dict
from pathlib import Path

# llama_cpp는 선택적 의존성
try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

def _load_model(self):
    """GGUF 모델을 메모리에 로드합니다."""
    if not self.model_path.exists():
        raise FileNotFoundError(
            f"모델 파일을 찾을 수 없습니다: {self.model_path}\n"
            f"Hugging Face에서 GGUF 모델을 다운로드하세요."
        )
    
    print(f"모델 로드 중: {self.model_path.name}")
    start_time = time.time()
    
    try:
        self.model = Llama(
            model_path=str(self.model_path),
            n_ctx=self.n_ctx,
            n_gpu_layers=self.n_gpu_layers,
            n_threads=self.n_threads,
            verbose=False
        )

        load_time = time.time() - start_time
        print(f"모델 로드 완료 ({load_time:.2f}초)")
        
        # 메모리 사용량 확인
        self._print_memory_usage()

    except Exception as e:
        print(f"모델 로드 실패: {e}")
        raise
        
def _print_memory_usage(self):
    """현재 메모리 사용량을 출력합니다."""
    import psutil
    
    process = psutil.Process()
    memory_mb = process.memory_info().rss / (1024**2)
    print(f"메모리 사용량: {memory_mb:.2f} MB")

def download_model_info(self) -> Dict[str, str]:
    """권장 모델 다운로드 정보를 반환합니다."""
    return {
        "1b_q4": "https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf",
        "3b_q4": "https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf",
        "7b_q4": "https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf",
        "note": "모델을 다운로드한 후 model_path에 파일 경로를 지정하세요."
    }
