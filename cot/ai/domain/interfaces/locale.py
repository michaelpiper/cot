# core/language/interfaces.py
from abc import ABC, abstractmethod
from typing import Dict
from ..entities import  FormattedBankingData


class ILocaleFormatter(ABC):
    @abstractmethod
    def format_banking_data(self, data: Dict) -> FormattedBankingData: ...
    
class IAsyncLocaleFormatter(ILocaleFormatter):
    @abstractmethod
    async def format_banking_data(self, data: Dict, locale: str) -> FormattedBankingData: ...
