from typing import Dict, List, Any
from .document import Document

class VectorStore:
    """Base vector store implementation"""
    
    def __init__(self):
        self.documents: Dict[str, Document] = {}
