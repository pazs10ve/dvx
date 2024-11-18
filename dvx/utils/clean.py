import re

def clean(text: str) -> str:
    """
    Clean text by applying lowercase conversion, whitespace normalization,
    and expanding shortened syllables.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text
    """
    text = lowercase(text)
    text = whitespace(text)
    text = expand(text)
    return text

def lowercase(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()

def whitespace(text: str) -> str:
    """
    Normalize whitespace by:
    - Removing extra newlines
    - Removing leading/trailing whitespace
    - Replacing multiple spaces with single space
    """
    text = text.strip()
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def expand(text: str) -> str:
    """
    Expand common contractions and shortened syllables.
    """
    contractions = {
        "aren't": "are not",
        "can't": "cannot",
        "couldn't": "could not",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'll": "he will",
        "he's": "he is",
        "i'd": "i would",
        "i'll": "i will",
        "i'm": "i am",
        "i've": "i have",
        "isn't": "is not",
        "it's": "it is",
        "let's": "let us",
        "shouldn't": "should not",
        "that's": "that is",
        "there's": "there is",
        "they'd": "they would",
        "they'll": "they will",
        "they're": "they are",
        "they've": "they have",
        "we'd": "we would",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what's": "what is",
        "where's": "where is",
        "who's": "who is",
        "won't": "will not",
        "wouldn't": "would not",
        "you'd": "you would",
        "you'll": "you will",
        "you're": "you are",
        "you've": "you have"
    }
    
    pattern = re.compile(r'\b(' + '|'.join(contractions.keys()) + r')\b', re.IGNORECASE)
    
    def replace(match):
        word = match.group(0)
        return contractions.get(word.lower(), word)   
    return pattern.sub(replace, text)

text = """Big data refers to large, diverse sets of information that grow at ever-increasing 
rates. It encompasses the volume of information, the velocity or speed at which it 
is created and collected, and the variety or scope of the data points being 
covered.

Data Science continues to be a driving force in many industries, offering insights 
that can lead to better decisions and optimized outcomes. It remains an evolving 
field that incorporates the latest technological advancements.
"""

#print(clean(text))