from abc import ABC, abstractmethod
import numpy as np

class BaseEncoder(ABC):
    """Abstract base class for different embedding models"""
    
    @abstractmethod
    def encode(self, text: str) -> np.ndarray:
        """Convert text to vector embedding"""
        pass
