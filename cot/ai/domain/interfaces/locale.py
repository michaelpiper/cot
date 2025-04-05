# core/language/interfaces.py
from abc import ABC, abstractmethod
from typing import Dict, Optional
from ..entities import Translation, FormattedBankingData

class ILanguageDetector(ABC):
    @abstractmethod
    def detect(self, text: str) -> str: ...

class ILocaleFormatter(ABC):
    @abstractmethod
    def format_banking_data(self, data: Dict) -> FormattedBankingData: ...
