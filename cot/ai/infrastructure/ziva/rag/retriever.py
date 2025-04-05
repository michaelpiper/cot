from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo import UpdateOne
from sentence_transformers import SentenceTransformer
from typing import List
import hashlib

from ....domain.entities.embedding import RetrievedEmbedding

from ....domain.interfaces.vector_retriever import IVectorRetriever


class ZiVAVectorRetriever(IVectorRetriever):
    def __init__(self, connection_str: str):
        self.model_version = "all-MiniLM-L6-v2"
        model = SentenceTransformer(self.model_version)
        client = MongoClient(connection_str)
        db = client.get_default_database()
        collection = db.document_embeddings
        self.db = db
        self.model = model
        self.collection = collection
    def create_index(self):
        self.create_document_embeddings_index()
        self.create_unique_index()
    def create_document_embeddings_index(self):
        """Create dynamic index for embeddings and text field for search """
        index_definition = {
            "mappings": {
                "dynamic": True,
                "fields": {
                    "embedding": {
                        "type": "knnVector",  # Specify vector index type
                        "dimensions": 384,  # Adjust this value based on your model's output
                        "similarity": "cosine"  # Cosine similarity for vector search
                    },
                    "text": {
                        "type": "text"  # Standard text search index
                    }
                }
            }
        }

        # Create the index in Atlas Search
        self.db.command({
            "createIndexes": "document_embeddings",  # Your collection name
            "indexes": [{
                "name": "document_embeddings",  # Give your index a name
                "key": {},  # No specific key here, as we define mappings directly
                "search": index_definition  # Apply the dynamic mapping as cosmos search options
            }]
        })

        # print("Index created successfully.")
        
    def create_unique_index(self):
        """ Create a text index (or other fields as required) """
        self.collection.create_index(
            [("content_hash", 1)], 
            unique=True, 
            name="content_hash_idx"
        )
    def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for query/documents"""
        return self.model.encode(text).tolist()

    def retrieve(self, query: str, top_k: int = 3, **kwargs) -> List[RetrievedEmbedding]:
        """Hybrid search (vector + metadata filtering)"""
        query_embedding = self.embed_text(query)
        should_filter = False
        filters = {"compound": {"must": []}}
        if "document_type" in kwargs:
            should_filter = True
            filters["compound"]["must"].append(
                {
                    "equals": {
                        "path": "metadata.document_type",
                        "value": kwargs.get("document_type"),
                    }
                }
            )  # Document type filtering
        if "locale" in kwargs:
            should_filter = True
            filters["compound"]["must"].append(
                {"equals": {"path": "metadata.locale", "value": kwargs.get("locale")}}
            )  # Multilingual filtering
        if "locales" in kwargs and isinstance(kwargs.get("locales"), list):
            should_filter = True
            filters["compound"]["must"].append(
                {"in": {"path": "metadata.locale", "value": kwargs.get("locales")}}
            )  # Multilingual filtering
        search_stage = {
            "$search": {
                "index": "document_embeddings",
                "knnBeta": {
                    "path": "embedding",  # Must match field storing vectors
                    "vector": query_embedding,  # Float list
                    "k": top_k,
                },
            }
        }
        if should_filter:
            search_stage["$search"]["filter"] = filters
        # Vector + metadata hybrid search
        results = self.collection.aggregate(
            [
                search_stage,
                {
                    "$project": {
                        "_id": 0,
                        "text": 1,
                        "metadata": 1,
                        "score": {"$meta": "searchScore"},
                    }
                },
            ]
        )

        return [RetrievedEmbedding.from_dict(embedding) for embedding in  list(results)]

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
                    "last_updated": datetime.now(timezone.utc),
                },
                "$set": {  # Always update these fields
                    "model_version": self.model_version,
                    "is_current": True,
                },
            },
            upsert=True,
        )

        result = self.collection.bulk_write([update_op])
        return {
            "inserted_id": result.upserted_ids.get(0),
            "existing_doc": result.matched_count > 0,
        }
