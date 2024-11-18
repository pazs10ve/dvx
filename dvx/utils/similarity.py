import numpy as np
from transformers import AutoTokenizer
from numpy.linalg import norm
from typing import Any, Tuple


class SemanticScore:
    def __init__(self,
        tokenizer: str = 'bert-base-uncased',
        metric: str = 'cosine',
        max_length: int = 100 
    ) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        self.max_length = max_length
        
        valid_metrics = ['dot_product', 'cosine', 'l1', 'l2']
        if metric not in valid_metrics:
            raise ValueError(f'Invalid metric. Must be one of {valid_metrics}')
        self.metric = metric
    
    def dot_product(self, A: np.ndarray, B: np.ndarray) -> float:
        """Dot Product is the sum after element wise multiplication of the arrays."""
        assert A.shape == B.shape, 'Arrays must have the same shape'
        return float(np.sum(A * B)) 

    def cosine(self, A: np.ndarray, B: np.ndarray) -> float:
        """
        Cosine similarity is defined as Dot Product normalized by the multiplication 
        of the norms of both tensors: cosine similarity = A . B / |A| |B|
        """
        assert A.shape == B.shape, 'Arrays must have the same shape'
        nA, nB = norm(A), norm(B)
        if nA == 0 or nB == 0:
            return 0.0
        return float(self.dot_product(A, B) / (nA * nB))

    def l1(self, A: np.ndarray, B: np.ndarray) -> float:
        """L1 norm is the sum of absolute element-wise difference"""
        assert A.shape == B.shape, 'Arrays must have the same shape'
        return float(np.sum(np.abs(A-B)))

    def l2(self, A: np.ndarray, B: np.ndarray) -> float:
        """L2 norm is the root of sum of squared difference between elements"""
        assert A.shape == B.shape, 'Arrays must have the same shape'
        return float(np.sqrt(np.sum((A-B)**2)))

    def calculate_score(self, A: np.ndarray, B: np.ndarray) -> float:
        assert A.shape == B.shape, 'Arrays must have the same shape'
        
        metric_functions = {
            'dot_product': self.dot_product,
            'cosine': self.cosine,
            'l1': self.l1,
            'l2': self.l2
        }
        
        return metric_functions[self.metric](A, B)

    def calculate(self, A: str, B: str) -> float:
        A_encoded = self.tokenizer(A, return_tensors='np')['input_ids'].squeeze()
        B_encoded = self.tokenizer(B, return_tensors='np')['input_ids'].squeeze()
        
        A_padded, B_padded = self.padding(A_encoded, B_encoded)
        
        return self.calculate_score(A_padded, B_padded)

    def padding(self, A: np.ndarray, B: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Pad or truncate sequences to max_length"""
        def pad_or_truncate(arr):
            if len(arr) > self.max_length:
                return arr[:self.max_length]
            elif len(arr) < self.max_length:
                return np.pad(arr, (0, self.max_length - len(arr)))
            return arr
            
        return pad_or_truncate(A), pad_or_truncate(B)
