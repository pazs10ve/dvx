from dvx.utils.chunking import fixed_size_chunk, sentence_based_chunk, paragraph_based_chunk, semantic_sentence_chunk
from dvx.utils.overlap import fixed_size_overlap, sentence_overlap, paragraph_overlap, semantic_sentence_overlap
from dvx import processors


def read_pdf(path : str, ) -> str:
    from dvx.processors.pdf import read
    content = read(path)
    return content

def read_docx(path : str) -> str:
    from dvx.processors.word import read
    content = read(path)
    return content

def read_txt(path : str) -> str:
    from dvx.processors.text import read
    content = read(path)
    return content

def chunk(content : str, chunking : str = 'semantic_sentence_chunk') -> str:
    if content == None:
        raise 'Invalid text provided'
    elif chunking == 'fixed_size_chunk':
        chunking = fixed_size_chunk
    elif chunking == 'sentence_based_chunk':
        chunking = sentence_based_chunk
    elif chunking == 'paragraph_based_chunk':
        chunking = paragraph_based_chunk
    elif chunking == 'semantic_sentence_chunk':
        chunking = semantic_sentence_chunk



def read_document(path : str, chunking : str = None, overlap : str = None, metric : str = 'cosine', chunk_size : int = None) -> str:
    if path.endswith('pdf'):
        content = read_pdf(path)
        return content
    elif path.endswith('docx'):
        content = read_docx(path)
        return content
    elif path.endswith('txt'):
        content = read_txt(path)
        return content
    else:
        raise 'Invalid document provided.'
    

def parse(folder_path : str):
    pass



path = r'data\MonoFormer.pdf'
content = read_document(path)
print(content)