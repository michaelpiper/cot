from abc import ABC, abstractmethod
from typing import Optional
from ..entities import Translation

class ITranslator(ABC):
    @abstractmethod
    def translate(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> str: ...
class IAsyncTranslator(ITranslator):
    @abstractmethod
    async def translate(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> str: ...

class ITranslationCache(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Translation]: ...
    
    @abstractmethod
    def set(self, key: str, translation: Translation) -> None: ...
    
class IAsyncTranslationCache(ITranslationCache):
    @abstractmethod
    async def get(self, key: str) -> Optional[Translation]: ...
    
    @abstractmethod
    async def set(self, key: str, translation: Translation) -> None: ...