from typing import List

from pymongo import database
from sentence_transformers import SentenceTransformer
from ..entities.embedding import RetrievedEmbedding


class IVectorRetriever:
    model: SentenceTransformer
    collection: database.Collection
        
       
    def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for query/documents"""
    
    def retrieve(self, query: str, top_k: int = 3, **kwargs) -> List[RetrievedEmbedding]:
        """Hybrid search (vector + metadata filtering)"""

    def _generate_document_hash(self, text: str, metadata: dict) -> str:
        """Generate SHA-256 hash of content + critical metadata"""
       
    
    def add_document(self, text: str, metadata: dict) -> dict:
        """Smart document insertion with hash checking"""
       