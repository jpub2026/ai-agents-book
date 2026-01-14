"""
세션 관리 시스템
대화와 시스템 상태를 저장하고 복원합니다
"""
import json
from datetime import datetime
from pathlib import Path

class SessionManager:
    def __init__(self, dir: str = "./sessions"):
        self.dir = Path(dir)
        self.dir.mkdir(exist_ok=True)
    
    def save(self, data: dict) -> str:
        """세션을 파일로 저장"""
        filename = f"session_{datetime.now():%Y%m%d_%H%M%S}.json"
        filepath = self.dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        return str(filepath)
    
    def load(self, filepath: str) -> dict:
        """저장된 세션 복원"""
        with open(filepath, 'r') as f:
            return json.load(f)
