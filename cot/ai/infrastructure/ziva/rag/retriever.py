import datetime
import os
from pymongo import MongoClient
from pymongo import UpdateOne
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import hashlib

from ....domain.interfaces.vector_retriever import IVectorRetriever

class ZiVAVectorRetriever(IVectorRetriever):
    def __init__(self):
        self.model_version="all-MiniLM-L6-v2"
        model = SentenceTransformer(self.model_version)
        client = MongoClient(os.getenv("MONGO_URI"))
        db = client.banking_rag
        collection = db.document_embeddings
        self.model = model
        self.collection = collection
       
        
        
    def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for query/documents"""
        return self.model.encode(text).tolist()
    
    def retrieve(self, query: str, top_k: int = 3, locale=None) -> List[Dict]:
        """Hybrid search (vector + metadata filtering)"""
        query_embedding = self.embed_text(query)
        
        # Vector + metadata hybrid search
        results = self.collection.aggregate([
            {
                "$vectorSearch": {
                    "index": "document_embeddings",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 50,
                    "limit": top_k,
                    "filter": {
                        "locale": {"$in": ["en", "fr"]},  # Multilingual filtering
                        "document_type": "banking_policy"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "text": 1,
                    "metadata": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ])
        
        return list(results)

    def _generate_document_hash(self, text: str, metadata: dict) -> str:
        """Generate SHA-256 hash of content + critical metadata"""
        hash_input = f"{text}-{metadata.get('document_type')}-{metadata.get('locale')}"
        return hashlib.sha256(hash_input.encode()).hexdigest()
    
    def add_document(self, text: str, metadata: dict) -> dict:
        """Smart document insertion with hash checking"""
        doc_hash = self._generate_document_hash(text, metadata)
        embedding = self.embed_text(text)
        
        update_op = UpdateOne(
            {"content_hash": doc_hash},
            {
                "$setOnInsert": {  # Only set these on new inserts
                    "text": text,
                    "embedding": embedding,
                    "content_hash": doc_hash,
                    "metadata": metadata,
                    "last_updated": datetime.utcnow()
                },
                "$set": {  # Always update these fields
                    "model_version": self.model_version,
                    "is_current": True
                }
            },
            upsert=True
        )
        
        result = self.collection.bulk_write([update_op])
        
        return {
            "inserted_id": result.upserted_id,
            "existing_doc": result.matched_count > 0
        }
