from typing import Dict, Any

def _check_gpu(self) -> bool:
    """CUDA GPU 사용 가능 여부를 확인합니다."""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        # llama.cpp의 GPU 지원 확인
        try:
            from llama_cpp import llama_cpp
            return hasattr(llama_cpp, 'LLAMA_SUPPORTS_GPU_OFFLOAD')
        except:
            return False
        
def _select_model_config(self) -> Dict[str, Any]:
    """메모리 용량에 따라 적절한 GGUF 모델을 선택합니다."""
    memory_gb = self.device_profile["memory_gb"]
    has_gpu = self.device_profile["gpu_available"]
    
    if memory_gb < 4:
        return {
            "model_file": "llama-3.2-1b-q4_k_m.gguf",
            "n_ctx": 512,
            "n_gpu_layers": 0,
            "n_threads": 2
        }
    elif memory_gb < 8:
        return {
            "model_file": "llama-3.2-3b-q4_k_m.gguf",
            "n_ctx": 1024,
            "n_gpu_layers": 10 if has_gpu else 0,
            "n_threads": 4
        }
    elif memory_gb < 16:
        return {
            "model_file": "llama-3.2-7b-q4_k_m.gguf",
            "n_ctx": 2048,
            "n_gpu_layers": 20 if has_gpu else 0,
            "n_threads": 6
        }
    else:
        return {
            "model_file": "llama-3.2-7b-q5_k_m.gguf",
            "n_ctx": 4096,
            "n_gpu_layers": -1 if has_gpu else 0,
            "n_threads": 8
        }
        
def _determine_optimization(self) -> str:
    """리소스에 따라 최적화 전략을 결정합니다."""
    memory_gb = self.device_profile["memory_gb"]
    
    if memory_gb < 8:
        return "aggressive"
    elif memory_gb < 16:
        return "balanced"
    else:
        return "quality"
