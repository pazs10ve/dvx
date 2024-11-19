import re
from dvx.utils.chunking import sentence_based_chunk, fixed_size_chunk, paragraph_based_chunk, semantic_sentence_chunk
from docx import Document


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
    Extracts and cleans the entire text from a DOCX file while preserving the paragraph structure.
    
    Args:
        file_path (str): Path to the DOCX file.
    
    Returns:
        str: Cleaned, structured text from the DOCX file.
    """
    def fix_hyphenated_words(text):
        """
        Fix hyphenated words split across lines.
        """
        return re.sub(r'-\n(\w+)', r'\1', text)

    doc = Document(file_path)
    all_text = ""

    for paragraph in doc.paragraphs:
        paragraph_text = paragraph.text.strip()
        paragraph_text = fix_hyphenated_words(paragraph_text)
        if paragraph_text:
            all_text += paragraph_text + "\n\n" 

    return remove_garbled_text(all_text)


"""path = r'data\Research Proposals.docx'
content = read(path)

chunks = semantic_sentence_chunk(content, metric = 'cosine', cosine_threshold=0.3)

print(f"Total Chunks: {len(chunks)}\n")
for idx, chunk in enumerate(chunks, start=1):
    print(f"Chunk {idx}:\n\n{chunk}\n")
"""