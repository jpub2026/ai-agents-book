from typing import Dict, Any
from pathlib import Path

def get_runtime_config(self) -> Dict[str, Any]:
    """시스템의 전체 런타임 구성을 반환합니다."""
    model_path = self.model_dir / self.model_config["model_file"]
    
    return {
        "device": self.device_profile,
        "model": {
            **self.model_config,
            "full_path": str(model_path),
            "exists": model_path.exists()
        },
        "optimization": self.optimization_level,
        "features": {
            "cache_enabled": True,
            "mmap_enabled": True,
            "mlock_enabled": self.optimization_level == "quality",
            "gpu_offload": self.model_config["n_gpu_layers"] > 0,
            "quantization": self._get_quantization_type()
        }
    }

def _get_quantization_type(self) -> str:
    """모델 파일명에서 양자화 타입을 추출합니다."""
    model_file = self.model_config["model_file"]
    
    if "q4_k_m" in model_file.lower():
        return "Q4_K_M"
    elif "q5_k_m" in model_file.lower():
        return "Q5_K_M"
    elif "q8_0" in model_file.lower():
        return "Q8_0"
    elif "f16" in model_file.lower():
        return "F16"
    else:
        return "unknown"
