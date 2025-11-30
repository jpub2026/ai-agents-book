from typing import List
from dataclasses import dataclass, field

@dataclass
class Document:
    """RAG에서 사용하는 문서 클래스"""
    id: str
    title: str
    content: str
    metadata: dict = field(default_factory=dict)

def add_documents(self, documents: List[Document]):
    """문서를 추가하고 검색 가능하도록 인덱싱합니다."""
    chunks = []
    for doc in documents:
        doc_chunks = self._split_into_chunks(doc.content)
        for i, chunk in enumerate(doc_chunks):
            chunk_doc = Document(
                id=f"{doc.id}_chunk_{i}",
                title=doc.title,
                content=chunk,
                metadata={
                    **doc.metadata,
                    "chunk_index": i,
                    "total_chunks": len(doc_chunks)
                }
            )
            chunks.append(chunk_doc)

    self.documents.extend(chunks)
    
    texts = [doc.content for doc in self.documents]
    self.embeddings = self.vectorizer.fit_transform(texts)

def _split_into_chunks(self, text: str) -> List[str]:
    """텍스트를 오버랩이 있는 청크로 분할합니다."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), self.chunk_size - self.overlap):
        chunk = ' '.join(words[i:i + self.chunk_size])
        if chunk:
            chunks.append(chunk)
            
    return chunks
