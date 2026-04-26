from typing import List, Tuple, Optional
from dataclasses import dataclass
import numpy as np

@dataclass
class Document:
    """RAG 시스템에서 사용하는 문서 모델입니다."""
    id: str
    title: str
    content: str
    metadata: dict
    embedding: Optional[np.ndarray] = None
