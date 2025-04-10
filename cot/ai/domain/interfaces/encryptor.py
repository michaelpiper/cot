from abc import abstractmethod
from typing import Protocol

class IEncryptor(Protocol):
    """Abstract encryption interface defined in domain layer"""
    @abstractmethod
    def encrypt(self, data: str) -> str: ...
    
    @abstractmethod
    def decrypt(self, payload: str) -> str: ...