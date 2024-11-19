from dvx.utils.similarity import SemanticScore


def fixed_size_chunk(text: str, chunk_size: int = 50) -> list[str]:
    """Split text into chunks of a fixed size"""
    text = text.split()
    text = [' '.join(text[i:i+chunk_size]) for i in range(0, len(text), chunk_size)]
    return text


def sentence_based_chunk(text: str) -> list[str]:
    """Split text on the basis of sentences"""
    text = text.split('.')
    text = [''.join(t.strip()) + '.' for t in text if t.strip()] 
    return text


def paragraph_based_chunk(text: str) -> list[str]:
    """Split text on the basis of paragraphs"""
    text = text.split('\n\n')
    return [t.strip() for t in text if t.strip()] 


def semantic_similarity_score(sentence1: str, 
                            sentence2: str, 
                            tokenizer: str = 'bert-base-uncased', 
                            metric: str = 'cosine') -> float:  
    score = SemanticScore(tokenizer=tokenizer, metric=metric)
    score = score.calculate(sentence1, sentence2)
    return score


def semantic_sentence_chunk(text: str, 
                  tokenizer: str = 'bert-base-uncased', 
                  metric: str = 'cosine',
                  dot_product_threshold: float = 1000.0,
                  cosine_threshold: float = 0.5, 
                  l1_threshold: float = 10000.0,
                  l2_threshold: float = 1000.0,
                  chunk_size: int = 5) -> list[str]:
    """
    Split text on the basis of semantics
    
    Args:
        text: Input text to be chunked
        tokenizer: Name of the pre-trained tokenizer
        metric: Similarity metric to use ('dot_product', 'cosine', 'l1', 'l2')
        *_threshold: Threshold values for different metrics
        chunk_size: Maximum size of each chunk in sentences
    """
    if not text.strip():
        return []

    if metric == 'dot_product':
        threshold = dot_product_threshold
    elif metric == 'cosine':
        threshold = cosine_threshold
    elif metric == 'l1':
        threshold = l1_threshold
    elif metric == 'l2':
        threshold = l2_threshold
    else:
        raise ValueError(f'Invalid similarity metric: {metric}')

    sentences = sentence_based_chunk(text)
    if not sentences:
        return []

    chunks = []
    calc = SemanticScore(tokenizer=tokenizer, metric=metric)
    
    current_chunk = []
    current_size = 0
    
    for i in range(len(sentences)):
        if not sentences[i].strip():
            continue
            
        if not current_chunk:
            current_chunk.append(sentences[i])
            current_size = 1
            continue
            
        score = calc.calculate(current_chunk[-1], sentences[i])
        
        if metric in ['l1', 'l2']:
            is_similar = score < threshold
        else:
            is_similar = score > threshold
            
        if is_similar and current_size < chunk_size:
            current_chunk.append(sentences[i])
            current_size += 1
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentences[i]]
            current_size = 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


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
#sentence1 = "Big data refers to large, diverse sets of information that grow at ever-increasing rates."
#entence2 = "My love for you is undying."
#print(semantic_similarity_score(sentence1, sentence2))
"""tokenizer = 'bert-base-uncased'
metric = 'l1'

score = SemanticScore(tokenizer=tokenizer, metric=metric)
print(score.calculate(sentence1, sentence2))"""


#tokenizer = 'bert-base-uncased'
#metric = 'cosine'
#print(semantic_similarity_score(sentence1, sentence2, tokenizer=tokenizer, metric=metric))


"""chunks = semantic_sentence_chunking(sample_text, metric='cosine')
for i, chunk in enumerate(chunks):
    print(f'\nChunk {i+1}:')
    print(chunk)
    print('---')"""