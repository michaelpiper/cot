from typing import Dict, Any, Optional
from datetime import datetime

class RetrievedEmbedding:
    def __init__(
        self,
        text: str,
        score: float,
        metadata: dict = {},
    ):
        self.text = text
        self.score = score
        self.metadata = metadata
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RetrievedEmbedding": 
        """
        Creates an instance of Embedding from a dictionary.
        :param data: Dictionary with keys corresponding to the attributes of Embedding.
        :return: Embedding instance.
        """   
         # Ensure all necessary fields exist
        required_keys = ["text", "score"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required field: {key}")

       
        # Return the instance of Embedding
        return cls(
            text=data["text"],
            score=data["score"],
            metadata=data.get("metadata", {}),
        )

    def __repr__(self):
        return f"RetrievedEmbedding(text={self.text}, score={self.score})"
    
class TextEmbedding:
    def __init__(
        self,
        text: str,
        embedding: list,
        content_hash: str,
        model_version: str,
        is_current: bool,
        metadata: dict = {},
        last_updated: Optional[datetime] = None,
    ):
        self.text = text
        self.embedding = embedding
        self.content_hash = content_hash
        self.metadata = metadata
        self.last_updated = last_updated
        self.model_version = model_version
        self.is_current = is_current

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TextEmbedding":
        """
        Creates an instance of Embedding from a dictionary.
        :param data: Dictionary with keys corresponding to the attributes of Embedding.
        :return: Embedding instance.
        """
        # Ensure all necessary fields exist
        required_keys = ["text", "embedding", "content_hash", "model_version", "last_updated"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required field: {key}")

        # Convert last_updated to a datetime object if it's a string (assuming ISO format)
        last_updated = data.get("last_updated")
        if isinstance(last_updated, str):
            last_updated = datetime.fromisoformat(last_updated)

        # Return the instance of Embedding
        return cls(
            text=data["text"],
            embedding=data.get("embedding", []),
            content_hash=data.get("content_hash"),
            metadata=data.get("metadata", {}),
            last_updated=last_updated,
            model_version=data.get("model_version"),
            is_current=data.get("is_current") == True,
        )

    def __repr__(self):
        return f"TextEmbedding(text={self.text}, content_hash={self.content_hash})"
