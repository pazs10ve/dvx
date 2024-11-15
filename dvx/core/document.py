from dataclasses import dataclass
from typing import Dict, Any, Optional
import numpy as np

@dataclass
class Document:
    """Base document class to store original document and its metadata"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None
