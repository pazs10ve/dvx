import re
from dvx.utils.chunking import fixed_size_chunk, sentence_based_chunk, paragraph_based_chunk, semantic_sentence_chunk

def remove_garbled_text(text: str) -> str:
    """
    Remove garbled text, encoding artifacts, and symbols while preserving paragraph structure and newlines.
    
    Args:
        text (str): The raw text to clean.
    
    Returns:
        str: Cleaned text with garbled content removed, preserving paragraph structure.
    """
    text = re.sub(r'[^\x20-\x7E\n]+', '', text)
    text = re.sub(r'(\W|\d){4,}', '', text)  
    text = re.sub(r'[~`@#$%^&*+=|<>/\[\]\{\}_]', '', text)  
    text = re.sub(r'\b[a-zA-Z0-9]\b', '', text)
    
    return text


def read(file_path: str) -> str:
    """
    Extracts and cleans the entire text from a TXT file while preserving paragraph structure.
    
    Args:
        file_path (str): Path to the TXT file.
    
    Returns:
        str: Cleaned, structured text from the TXT file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        all_text = file.read()

    return remove_garbled_text(all_text)


"""path = r'data\message.txt'
content = read(path)

chunks = semantic_sentence_chunk(content)
print(f"Total Chunks: {len(chunks)}\n")
for idx, chunk in enumerate(chunks, start=1):
    print(f"Chunk {idx}:\n\n{chunk}\n")
"""