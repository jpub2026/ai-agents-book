from pathlib import Path
from typing import Dict, Any


class EdgeAdaptiveSystem:
    """디바이스 특성에 따라 자동으로 최적 설정을 선택합니다."""
    
    def __init__(self, model_dir: str = "./models"):
        self.model_dir = Path(model_dir)
        self.device_profile = self._detect_device_profile()
        self.model_config = self._select_model_config()
        self.optimization_level = self._determine_optimization()

    def _detect_device_profile(self) -> Dict[str, Any]:
        """현재 디바이스의 하드웨어 프로파일을 감지합니다."""
        import psutil
        import platform
        
        return {
            "cpu_count": psutil.cpu_count(),
            "memory_gb": psutil.virtual_memory().total / (1024**3),
            "platform": platform.system(),
            "architecture": platform.machine(),
            "gpu_available": self._check_gpu()
        }

    def _check_gpu(self) -> bool:
        """GPU 사용 가능 여부를 확인합니다."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def _select_model_config(self) -> Dict[str, Any]:
        """디바이스에 맞는 모델 설정을 선택합니다."""
        memory_gb = self.device_profile.get("memory_gb", 0)

        if memory_gb >= 16:
            return {"model_size": "large", "quantization": "4bit"}
        elif memory_gb >= 8:
            return {"model_size": "medium", "quantization": "4bit"}
        else:
            return {"model_size": "small", "quantization": "8bit"}

    def _determine_optimization(self) -> str:
        """최적화 수준을 결정합니다."""
        if self.device_profile.get("gpu_available"):
            return "gpu_accelerated"
        elif self.device_profile.get("cpu_count", 0) >= 8:
            return "multi_threaded"
        else:
            return "basic"
