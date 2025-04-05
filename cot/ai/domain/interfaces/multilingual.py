# domain/interfaces.py
from abc import ABC, abstractmethod
from typing import Dict
from ..entities import FormattedBankingData, TranslationRequest

class ILanguageDetector(ABC):
    @abstractmethod
    def detect(self, text: str) -> str: ...

class ITranslator(ABC):
    @abstractmethod
    def translate(self, request: TranslationRequest) -> str: ...

class ILocaleFormatter(ABC):
    @abstractmethod
    def format_banking_data(self, data: Dict, locale: str) -> FormattedBankingData: ...

class ILocalizationRepository[Entity:Dict[str,str]]:
    @abstractmethod
    def get_localized_terms(self, locale: str) -> Entity: ...
    
    
class IAsyncLanguageDetector(ILanguageDetector):
    @abstractmethod
    async def detect(self, text: str) -> str: ...

class IAsyncTranslator(ITranslator):
    @abstractmethod
    async def translate(self, request: TranslationRequest) -> str: ...

class IAsyncLocaleFormatter(ILocaleFormatter):
    @abstractmethod
    async def format_banking_data(self, data: Dict, locale: str) -> FormattedBankingData: ...

class IAsyncLocalizationRepository[Entity: Dict[str, str]](ILocalizationRepository[Entity]):
    @abstractmethod
    async def get_localized_terms(self, locale: str) -> Entity: ...