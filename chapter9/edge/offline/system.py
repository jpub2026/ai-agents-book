import sqlite3
import pickle
from pathlib import Path
from typing import Optional

class OfflineCapableSystem:
    """네트워크 없이도 동작하는 오프라인 시스템입니다."""
    
    def __init__(
        self,
        cache_dir: str = "./offline_cache",
        db_path: str = "./offline.db"
    ):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.db_path = Path(db_path)
        self._init_database()
