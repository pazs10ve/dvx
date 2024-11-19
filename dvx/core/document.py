from dvx.utils.chunking import fixed_size_chunk, sentence_based_chunk, paragraph_based_chunk, semantic_sentence_chunk
from dvx.utils.overlap import fixed_size_overlap, sentence_overlap, paragraph_overlap, semantic_sentence_overlap
from dvx import processors

import os


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


def validate_chunking(chunking : str = 'semantic_sentence_chunk') -> str:
    if chunking == 'fixed_size_chunk':
        return fixed_size_chunk
    elif chunking == 'sentence_based_chunk':
        return sentence_based_chunk
    elif chunking == 'paragraph_based_chunk':
        return paragraph_based_chunk
    elif chunking == 'semantic_sentence_chunk':
        return semantic_sentence_chunk
    else:
        raise 'Invalid chunking strategy provided'
    

def chunk(content : str, chunking : str = 'semantic_sentence_chunk') -> str:
    if content == None:
        raise 'Invalid text provided'
    
    chunking = validate_chunking(chunking)
    return chunking(content)


def validate_overlap(overlap : str = 'semantic_sentence_overlap') -> str:
    if overlap == 'fixed_size_overlap':
        overlap = fixed_size_overlap
    elif overlap == 'sentence_overlap':
        overlap = sentence_overlap
    elif overlap == 'paragraph_overlap':
        overlap = paragraph_overlap
    elif overlap == 'semantic_sentence_overlap':
        overlap = semantic_sentence_overlap
    else:
        raise 'Invalid overlap argument provided'
    
    
def overlap(chunks : list[str], overlap_type : str = 'semantic_sentence_overlap', overlap_size : int = 100):
    overlap_iter = validate_overlap(overlap_type)
    i = 0
    j = 1
    overlapped_chunks = []

    while j < len(chunks):
        text = semantic_sentence_overlap(chunks[i], chunks[j])
        i += 1
        j += 1
        overlapped_chunks.append(text)
    return overlapped_chunks


def read_document(path : str) -> str:
    if path.endswith('pdf'):
        content = read_pdf(path)

    elif path.endswith('docx'):
        content = read_docx(path)
    elif path.endswith('txt'):
        content = read_txt(path)
    else:
        raise 'Invalid document provided.'
    return content


def parse(folder_path : str, chunking : str = 'semantic_sentence_chunk'):
    validate_chunking(chunking)

    file_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    
    folder_chunks = []
    for path in file_list:
        content = read_document(path)
        chunks = chunk(content, chunking = chunking)
        folder_chunks.extend(chunks)

    return folder_chunks





"""path = r'data\MonoFormer.pdf'
content = read_document(path)
chunks = chunk(content, chunking = 'semantic_sentence_chunk')
print(f"Total Chunks: {len(chunks)}\n")
for idx, chunk in enumerate(chunks, start=1):
    print(f"Chunk {idx}:\n\n{chunk}\n")"""


folder_path = 'data'
chunking = 'paragraph_based_chunk'
chunks = parse(folder_path, chunking = chunking)
print(f"Total Chunks: {len(chunks)}\n")
overlap_type = 'semantic_sentence_overlap'
chunks = overlap(chunks, overlap_type=overlap_type)
print(f"Total Chunks: {len(chunks)}\n")
#for idx, chunk in enumerate(chunks, start=1):
 #   print(f"Chunk {idx}:\n\n{chunk}\n")