import PyPDF2
import re
from dvx.utils.clean import clean
from dvx.utils.chunking import sentence_based_chunk, fixed_size_chunk, paragraph_based_chunk, semantic_sentence_chunk


def is_prose_line(line: str) -> bool:
    """
    Check if a line appears to be normal prose text.
    Returns True if the line looks like regular text, False otherwise.
    """
    if not line.strip():
        return False  
    

    
    if re.match(r'^(figure|fig\.|table|tab\.|diagram|chart)\s*\d+', line.lower()):
        return False
    if re.match(r'^\s*(\d+[\.)]]|\*|\-|\u2022|\u2023|\u2043|[a-zA-Z][\.)]])\s+', line):
        return False
    if re.search(r'http[s]?://|www\.|@[a-zA-Z0-9]+\.[a-zA-Z]', line):
        return False
    
    if len(re.findall(r'[^a-zA-Z0-9\s.,!?()-]', line)) / len(line) > 0.1: 
        return False
    if re.search(r'\w+\s{2,}\w+\s{2,}\w+', line): 
        return False
    
    words = line.strip().split()
    if len(words) > 1 and sum(1 for word in words if word.isupper()) / len(words) > 0.5:
        return False
    
    return True


def remove_garbled_text(text: str) -> str:
    """
    Remove garbled text, encoding artifacts, and symbols while preserving newlines.
    
    Args:
        text (str): The raw text to clean.
    
    Returns:
        str: Cleaned text with garbled content removed.
    """
    text = re.sub(r'[^\x20-\x7E\n]+', '', text)  
    
    text = re.sub(r'(\W|\d){4,}', '', text)  
    text = re.sub(r'[~`@#$%^&*+=|<>/\[\]\{\}_]', '', text) 
    
    text = re.sub(r'\b[a-zA-Z0-9]\b', '', text)
    
    return text.strip()


def read(file_path: str) -> str:
    """
    Extracts and cleans the entire text from a PDF while preserving structure.
    
    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        str: Cleaned, structured text from the PDF.
    """
    def fix_hyphenated_words(text):
        """
        Fix hyphenated words split across lines.
        """
        return re.sub(r'-\n(\w+)', r'\1', text) 

    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        all_text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            page_text = fix_hyphenated_words(page_text)
            all_text += page_text + "\n" 
        
        return remove_garbled_text(all_text)


"""path = r'data\A GENERATIVE INFINITE GAME OF SIMULATION.pdf'
content = read(path)
chunks = semantic_sentence_chunk(content, metric = 'cosine', cosine_threshold=0.3)

print(f"Total Chunks: {len(chunks)}\n")
for idx, chunk in enumerate(chunks, start=1):
    chunk = clean(chunk)
    print(f"Chunk {idx}:\n\n{chunk}\n")
"""