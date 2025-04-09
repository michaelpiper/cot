# domain/interfaces.py
from abc import ABC, abstractmethod
from typing import Dict, List

from cot.ai.domain.interfaces.translation_cache import ITranslationCache
from ..entities import TranslationRequest


class ILanguageDetector(ABC):
    @abstractmethod
    def detect(self, text: str) -> str: ...


class ITranslator(ABC):
    @abstractmethod
    def translate(self, request: TranslationRequest) -> str: ...


class ILocalizationRepository[Entity: Dict[str, str]]:
    @abstractmethod
    def get_localized_terms(self, locale: str) -> Entity: ...


class IAsyncLanguageDetector(ILanguageDetector):
    @abstractmethod
    async def detect(self, text: str) -> str: ...


class IAsyncTranslator(ITranslator):
    @abstractmethod
    async def translate(self, request: TranslationRequest) -> str: ...


class IAsyncLocalizationRepository[Entity: Dict[str, str]](
    ILocalizationRepository[Entity]
):
    @abstractmethod
    async def get_localized_terms(self, locale: str) -> Entity: ...

class IUserInputUseCase:
    @abstractmethod
    def execute(
        self, text: str, user_locale: str, banking_terms: Dict[str, Dict[str, str]]
    ) -> Dict:...
class ITranslateUseCase:
    @abstractmethod
    def execute(self, request: TranslationRequest) -> str: ...
class ITranslationUseCase:
  
    @abstractmethod
    def execute(
        self,
        request: TranslationRequest,
        supported_languages: List[str] = [],
        banking_terms: Dict[str, Dict[str, str]] = {},
    ) -> str:...

class ITranslateTextUseCase:
    @abstractmethod
    def execute(self, text: str, *args, **kwargs) -> str: ...
class ITranslateBankingTermsUseCase:
    @abstractmethod
    def execute(
        self,
        text: str,
        detected_banking_terms: list[str],
        banking_terms: Dict[str, Dict[str, str]],
    ) -> str: ...
class IDetectLanguageUseCase:
    @abstractmethod
    def execute(
        self,
        text: str,
       *args,
       **kwargs,
    ) -> str: ...

class IFindBankingTermsUseCase:
    def execute(
        self,
        text: str,
        target_lang: str,
        banking_terms: Dict[str, Dict[str, str]],
    ) -> List: ...
