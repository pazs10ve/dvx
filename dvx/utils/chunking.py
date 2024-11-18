from typing import Any, Tuple
import numpy as np
from numpy.linalg import norm
from transformers import AutoTokenizer


def fixed_size_chunk(text: str, chunk_size: int = 50) -> list[str]:
    """Split text into chunks of a fixed size"""
    text = text.split()
    text = [' '.join(text[i:i+chunk_size]) for i in range(0, len(text), chunk_size)]
    return text


def sentence_based_chunk(text : str) -> list[str]:
    """Split text on the basis of sentences"""
    text = text.split('.')
    text = [''.join(t)+'.' for t in text]
    return text


def paragraph_based_chunk(text : str) -> list[str]:
    """Split text on the basis of paragraphs"""
    text = text.split('\n\n')
    return text


def semantic_similarity_score(sentence1 : str, 
                              sentence2 : str, 
                              tokenizer : str = 'bert-base-uncased', 
                              metric : str = 'cosine') -> int:
    score = SemanticScore(tokenizer=tokenizer, metric=metric)
    score = score.calculate(sentence1, sentence2)
    return score


def semantic_chunk(text : str, 
                   tokenizer : str = 'bert-base-uncased', 
                   metric : str = 'cosine',
                   dot_product_threshold : int = 1000, 
                   cosine_threshold : int = 0.5, 
                   l1_threshold : int = 10000,
                   l2_threshold : int = 1000,
                   chunk_size : int = 5) -> list[str]:
    """Split text on the basis of semantics"""

    if metric == 'dot_product':
        threshold = dot_product_threshold
    elif metric == 'cosine':
        threshold = cosine_threshold
    elif metric == 'l1':
        threshold = l1_threshold
    elif metric == 'l2':
        threshold = l2_threshold
    else:
        raise 'Not a valid similarity metric provided.'

    text = sentence_based_chunk(text)

    chunks = []
    calc = SemanticScore(tokenizer=tokenizer, metric=metric)
    i = 0
    while i < len(text)-1:
        j = i+1
        chunk = text[i]
        while j < len(text):
            score = calc.calculate(text[i], text[j])
            if score > threshold and len(chunk) < chunk_size:
                chunk += text[j]
                j += 1
            else:
                i = j+1 
                j = i+1
                if chunk != '':
                    chunks.append(chunk)
                    chunk = text[i] if i < len(text) else ''

    return chunks


def multi_modal_chunk(text : str, images = None, tables = None) -> Any:
    """Split text, separates images and tables"""
    pass 


class SemanticScore:
    def __init__(self,
        tokenizer : str = 'bert-base-uncased',
        metric : str = 'cosine',
        max_length : str = 100
    ) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        self.max_length = max_length
        
        if metric in ['dot_product', 'cosine', 'l1', 'l2']:
            self.metric = metric
        else:
            raise 'Not a valid metric provided'
    
    def dot_product(self, A : np.ndarray, B : np.ndarray) -> int:
        """ Dot Product is the sum after element wise multiplication of the arrays. """
        assert (A.shape == B.shape), 'The shape of the arrays should be same'
        return np.sum(A * B)

    def cosine(self, A : np.ndarray, B : np.ndarray) -> int:
        """ Cosine similarity is defined as Dot Product normalized by the multiplication of the norms of both tensors

                cosine similarity = A . B / |A| |B| 
        """
        assert (A.shape == B.shape), 'The shape of the arrays should be same'
        assert (norm(A) != 0 and norm(B) != 0), 'Division by zero is not possible!'
        return self.dot_product(A, B) / (norm(A)*norm(B))


    def l1(self, A : np.ndarray, B : np.ndarray) -> int:
        """ L1 norm is the sum of absolute element-wise difference """
        assert (A.shape == B.shape), 'The shape of the arrays should be same'
        return np.sum(np.abs(A-B))

    def l2(self, A : np.ndarray, B : np.ndarray) -> int:
        """ L2 norm is the root of sum of squared difference between elements"""
        assert (A.shape == B.shape), 'The shape of the arrays should be same'
        return np.sqrt(np.sum((A-B)**2))

    def calculate_score(self, A : np.ndarray, B : np.ndarray) -> int:
        assert (A.shape == B.shape), 'The shape of the arrays should be same'
        if self.metric == 'dot_product':
            return self.dot_product(A, B)
        elif self.metric == 'cosine':
            return self.cosine(A, B)
        elif self.metric == 'l1':
            return self.l1(A, B)
        elif self.metric == 'l2':
            return self.l2(A, B)


    def calculate(self, A : str, B : str) -> int:
        #print(A, B)
        A, B = self.tokenizer(A), self.tokenizer(B)
        A, B = self.padding(A['input_ids'], B['input_ids'])
        return self.calculate_score(A, B)
        

    def padding(self, A : np.ndarray, B : np.ndarray) -> Tuple[np.ndarray, np.ndarray]:

        if len(A) > self.max_length:
            diff1 = np.abs(len(A) - self.max_length)
            A = A[:self.max_length]
        elif len(A) < self.max_length:
            diff1 = np.abs(len(A) - self.max_length)
            pad1 = np.zeros(diff1)
            A = np.concat((A, pad1))

        if len(B) > self.max_length:
            diff2 = np.abs(len(B) - self.max_length)
            B = B[:self.max_length]
        elif len(B) < self.max_length:
            diff2 = np.abs(len(B) - self.max_length)
            pad2 = np.zeros(diff2)
            B = np.concat((B, pad2))
        
        return A, B


sample_text = """
Introduction

Data Science is an interdisciplinary field that uses scientific methods, processes,
 algorithms, and systems to extract knowledge and insights from structured and 
 unstructured data. It draws from statistics, computer science, machine learning, 
 and various data analysis techniques to discover patterns, make predictions, and 
 derive actionable insights.

Data Science can be applied across many industries, including healthcare, finance,
 marketing, and education, where it helps organizations make data-driven decisions,
  optimize processes, and understand customer behaviors.

Overview of Big Data

Big data refers to large, diverse sets of information that grow at ever-increasing 
rates. It encompasses the volume of information, the velocity or speed at which it 
is created and collected, and the variety or scope of the data points being 
covered.

Data Science Methods

There are several important methods used in Data Science:

1. Regression Analysis
2. Classification
3. Clustering
4. Neural Networks

Challenges in Data Science

- Data Quality: Poor data quality can lead to incorrect conclusions.
- Data Privacy: Ensuring the privacy of sensitive information.
- Scalability: Handling massive datasets efficiently.

Conclusion

Data Science continues to be a driving force in many industries, offering insights 
that can lead to better decisions and optimized outcomes. It remains an evolving 
field that incorporates the latest technological advancements.
"""

#chunks = semantic_chunk(sample_text)
#print(chunks)
#for chunk in chunks:
 #   print(chunk, '\n---\n')
sentence1 = "Big data refers to large, diverse sets of information that grow at ever-increasing rates."
sentence2 = "My love for you is undying."
#print(semantic_similarity_score(sentence1, sentence2))
"""tokenizer = 'bert-base-uncased'
metric = 'l1'

score = SemanticScore(tokenizer=tokenizer, metric=metric)
print(score.calculate(sentence1, sentence2))"""


#tokenizer = 'bert-base-uncased'
#metric = 'cosine'
#print(semantic_similarity_score(sentence1, sentence2, tokenizer=tokenizer, metric=metric))
chunks = semantic_chunk(sample_text)

#print(chunks)
for chunk in enumerate(chunks):
    
    print(f'chunk {chunk[0]+1}')
    print(chunk[1], '\n---\n')
