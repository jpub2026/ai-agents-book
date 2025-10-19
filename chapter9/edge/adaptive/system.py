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
