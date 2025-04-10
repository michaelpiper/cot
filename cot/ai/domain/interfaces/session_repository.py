from abc import ABC, abstractmethod
from ..models.session import Session
class ISessionManager:
    @abstractmethod
    async def get(self, session_id: str) -> Session:...
    @abstractmethod
    async def save(self, session: Session):...
    
class ISessionRepository(ABC):
    @abstractmethod
    async def get(self, session_id: str) -> Session: ...
    
    @abstractmethod
    async def save(self, session: Session): ...