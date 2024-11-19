from typing import Tuple
from dvx.utils.chunking import sentence_based_chunk, paragraph_based_chunk, semantic_sentence_chunk

def fixed_size_overlap(text1 : str, text2 : str, overlap_size : int = 20) -> Tuple[str, str]:
    """Return overlapping chunks of fixed dimensions with a specified overlap token size."""
    overlap = text1[-overlap_size:]
    return overlap+text2
    

def sentence_overlap(text1 : str, text2 : str, overlap_size : int = 1) -> Tuple[str, str]:
    """Return overlapping chunks of sentence based chunks with a specified overlap token size."""
    sentences = sentence_based_chunk(text1)
    overlap = ''.join(i for i in sentences[-overlap_size:])
    return overlap+text2


def paragraph_overlap(text1 : str, text2 : str, overlap_size : int = 1) -> Tuple[str, str]:
    """Return overlapping chunks of paragraph based chunks with a specified overlap token size."""
    paragraphs = paragraph_based_chunk(text1)
    overlap = ''.join(i for i in paragraphs[-overlap_size:])
    return overlap+text2
    

def semantic_sentence_overlap(text1 : str, text2 : str, overlap_size : int = 100) -> Tuple[str, str]:
    """Return overlapping chunks of semantic chunks with a specified overlap token size."""
    semantic = semantic_sentence_chunk(text1)
    overlap = text1[-overlap_size:]
    return overlap+text2
    


text1 = """Big data refers to large, diverse sets of information that grow at ever-increasing 
rates. It encompasses the volume of information, the velocity or speed at which it 
is created and collected, and the variety or scope of the data points being 
covered.

Data Science continues to be a driving force in many industries, offering insights 
that can lead to better decisions and optimized outcomes. It remains an evolving 
field that incorporates the latest technological advancements.
"""

text2 = """Vision Arena is a leaderboard solely based on anonymous voting of model outputs and is updated continuously. 
In this arena, the users enter an image and a prompt, and outputs from two different models are sampled anonymously, 
then the user can pick their preferred output. 
This way, the leaderboard is constructed solely based on human preferences.

It draws from statistics, computer science, machine learning, 
 and various data analysis techniques to discover patterns, make predictions, and 
 derive actionable insights.
"""

text3 = """Open VLM Leaderboard, is another leaderboard where various vision language models 
are ranked according to these metrics and average scores. 
You can also filter models according to model sizes, proprietary or open-source licenses,
 and rank for different metrics.
 
 
 There are different benchmarks to evaluate vision language models that you may come across in the leaderboards. 
 We will go through a few of them.There are various ways to pretrain a vision language model.
   The main trick is to unify the image and text representation and feed it to a text decoder for generation
 """

#text = semantic_sentence_overlap(text2, text1)
#print(text)
