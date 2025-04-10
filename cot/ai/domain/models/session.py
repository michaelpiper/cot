from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Self
import uuid
import copy  # For deep copying


@dataclass
class Session:
    session_id: str
    created_at: datetime
    last_accessed: datetime
    data: Dict

    def __init__(
        self,
        session_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        last_accessed: Optional[datetime] = None,
        data: Dict = {},
    ):
        self.session_id = uuid.uuid4().hex if not session_id else session_id
        self.created_at = datetime.now(timezone.utc) if not created_at else created_at
        self.last_accessed = (
            datetime.now(timezone.utc) if not last_accessed else last_accessed
        )
        self.data = {} if not data else data

    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        return cls(**data)
    
    def get(self, key: str = None, deep_copy: bool = False) -> Optional[Any]:
        """
        Get a value from the session data using dot notation for nested access.
        Supports quoted segments for special characters (e.g., "user.\"first.name\".email").
        
        Args:
            key: Dot-separated path to the value. Supports quoted segments.
                If None, returns a deep copy of all session data.
            deep_copy: If True, returns a deep copy that cannot modify original data.
        
        Returns:
            The requested value or None if not found. Returns all data if key is None.
        """
        # Validate input type
        if key is not None and not isinstance(key, str):
            raise TypeError(f"Key must be str or None, got {type(key).__name__}")

        # Return all data if no key specified
        if key is None:
            return copy.deepcopy(self.data) if deep_copy else self.data
        
        # Parse path segments handling quoted values
        path = []
        current_segment = []
        in_quotes = False
        quote_char = None
        escape = False
        
        for char in key:
            if escape:
                current_segment.append(char)
                escape = False
            elif char == '\\':
                escape = True
            elif in_quotes:
                if char == quote_char:
                    in_quotes = False
                    path.append(''.join(current_segment))
                    current_segment = []
                else:
                    current_segment.append(char)
            elif char in ('"', "'"):
                in_quotes = True
                quote_char = char
            elif char == '.' and not in_quotes:
                if current_segment:
                    path.append(''.join(current_segment))
                    current_segment = []
            else:
                current_segment.append(char)
        
        if current_segment:
            path.append(''.join(current_segment))
        
        # Traverse nested structure
        current = self.data
        
        try:
            for segment in path:
                if isinstance(current, dict):
                    current = current[segment]
                elif isinstance(current, (list, tuple)) and segment.isdigit():
                    current = current[int(segment)]
                else:
                    return None
            return copy.deepcopy(current) if deep_copy else current
        except (KeyError, IndexError, TypeError, ValueError):
            return None
    def set(self, key: str, value: Any, create_missing: bool = False) -> bool:
        """
        Set a value in the session data using dot notation for nested access.
        Supports:
        - Quoted segments ("user.\"first.name\"")
        - Array appending ("users.[]")
        - Automatic collection creation (with create_missing=True)
        
        Args:
            key: Dot-separated path to the value
            value: Value to set/append
            create_missing: If True, creates missing dictionaries/arrays in the path
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            TypeError: If key is not a string
            ValueError: If path is invalid and create_missing=False
        """
        # Validate input
        if not isinstance(key, str):
            raise TypeError(f"Key must be str, got {type(key).__name__}")
        if not key:
            raise ValueError("Key cannot be empty")

        # Parse path segments
        path: List[str] = []
        current_segment = []
        in_quotes = False
        quote_char = None
        escape = False
        
        for char in key:
            if escape:
                current_segment.append(char)
                escape = False
            elif char == '\\':
                escape = True
            elif in_quotes:
                if char == quote_char:
                    in_quotes = False
                    path.append(''.join(current_segment))
                    current_segment = []
                else:
                    current_segment.append(char)
            elif char in ('"', "'"):
                in_quotes = True
                quote_char = char
            elif char == '.' and not in_quotes:
                if current_segment:
                    path.append(''.join(current_segment))
                    current_segment = []
            else:
                current_segment.append(char)
        
        if current_segment:
            path.append(''.join(current_segment))
        
        current = self.data
        try:
            # Traverse to parent
            for segment in path[:-1]:
                if segment == '[]':
                    raise ValueError("Array append syntax only allowed at end of path")
                    
                if isinstance(current, dict):
                    if segment not in current and create_missing:
                        if segment == path[-2] and path[-1] == "[]":
                            current[segment] = []
                        else:
                            current[segment] = {}
                    current = current[segment]
                elif isinstance(current, list):
                    if  segment.isdigit():
                        current = current[int(segment)]
                    else:
                        return False
                else:
                    return False
            
            # Handle final segment
            final_segment = path[-1]
            
            # Array append case
            if final_segment == '[]':
                if isinstance(current, list):
                    current.append(value)
                    return True
                return False
            
            # Normal set case
            if isinstance(current, dict):
                current[final_segment] = value
                return True
            elif isinstance(current, list) and final_segment.isdigit():
                current[int(final_segment)] = value
                return True
            
            return False
            
        except (KeyError, IndexError, TypeError, ValueError):
            return False
@dataclass
class AuthContext:
    access_token: str
    scopes: list[str]
    expires_at: datetime

    def __init__(self, access_token: str, expires_at: datetime, scopes: list[str] = []):
        self.access_token: str = access_token
        self.scopes: list[str] = [] if not scopes else scopes
        self.expires_at: datetime = expires_at


class BankingSession(Session):
    @classmethod
    def from_session(cls, session: Session) -> Self:
        return cls(
            session_id=session.session_id,
            created_at=session.created_at,
            last_accessed=session.last_accessed,
            data=session.data,
        )

    def __init__(
        self,
        session_id: str,
        created_at: Optional[datetime] = None,
        last_accessed: Optional[datetime] = None,
        data: Optional[Dict] = None,
    ):
        data = data or {
            "conversation": [],
            "user": None,  # Stores user profile reference
            "auth": {  # Encrypted sensitive data
                "access_token": None,
                "refresh_token": None,
                "token_expiry": None,
                "scope": [],
            },
            "banking_context": {  # Financial session state
                "current_flow": None,  # e.g., "money_transfer"
                "flow_state": {},  # Multi-step process data
                "last_transaction": None,
            },
            "nlp_context": {  # Conversation intelligence
                "detected_intent": None,
                "entities": [],
                "sentiment": 0.5,
                "language": "en",
            },
            "rag_context": {  # Retrieval-Augmented Generation
                "last_retrieved": [],
                "document_hashes": [],
                "knowledge_graph": {},
            },
        }
        super(BankingSession, self).__init__(
            session_id,
            created_at,
            last_accessed,
            data,
        )
