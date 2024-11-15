from typing import Dict, Any
import pandas as pd
import os
from datetime import datetime
import hashlib
from pathlib import Path


class DocumentMetaData:
    """Base document meta class to infer the metadata of the document"""
    def __init__(self):
        self.columns = ['id', 'path', 'created_on', 'modified_on', 'size', 'title']
        self.df = pd.DataFrame(columns=self.columns)
        

    def _parse_doc_type(self, path: str) -> str:
        if self._check_txt(path):
            return 'txt'
        elif self._check_pdf(path):
            return 'pdf'
        elif self._check_docx(path):
            return 'docx'
        else:
            raise ValueError("Couldn't infer the document type!")

    def _check_pdf(self, path: str) -> bool:
        return path.endswith('.pdf')

    def _check_txt(self, path: str) -> bool:
        return path.endswith('.txt')

    def _check_docx(self, path: str) -> bool:
        return path.endswith('.docx')

    def _create_id(self, path: str) -> str:
        return hashlib.md5(os.path.basename(path).encode()).hexdigest()

    def _get_datetime(self) -> str:
        return datetime.now().isoformat()

    def _create_metadata(self, path: str) -> Dict[str, Any]:
        file_size = os.path.getsize(path) / (1024 * 1024)
        file_name = os.path.basename(path)
        title, _ = os.path.splitext(file_name)

        return {
            'id': self._create_id(path),
            'path': path,
            'created_on': self._get_datetime(),
            'modified_on': self._get_datetime(),
            'size': file_size,
            'title': title
        }
    
    def add_meta(self, path : str) -> None:
        if path not in self.df['path'].values:
            self.path = path
            self.type = self._parse_doc_type(path)
            meta_data = self._create_metadata(path)
            self.df = pd.concat([self.df, pd.DataFrame([meta_data])])
        else:
            print(f'The document {path} already exists in the database')

    def get_meta(self, idx: int) -> Dict[str, Any]:
        return self.df.iloc[idx].to_dict()
    



def generate_metadata(folder_path : str, metadoc : DocumentMetaData = None) -> DocumentMetaData:
    if metadoc == None:
        metadoc = DocumentMetaData()
    for file in os.listdir(folder_path):
        if file.endswith('.txt') or file.endswith('.pdf') or file.endswith('.docx'):
            file_path = os.path.join(folder_path, file)
            metadoc.add_meta(file_path) 

    return metadoc


#print(generate_metadata('data').df)
#metadoc = DocumentMetaData()
#print(generate_metadata('data', metadoc).df)
"""  metadoc = DocumentMetaData()
metadoc.add_meta(r'data\MonoFormer.pdf')
metadoc.add_meta(r'data\BIORAG.pdf')
metadoc.add_meta(r'data\ARecipe For Building a Compliant Real Estate Chatbot.pdf')
print(metadoc.df) """


