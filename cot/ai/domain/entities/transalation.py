# domain/entities.py
from dataclasses import dataclass
import datetime
from typing import Dict, List, Optional

@dataclass
class TranslationRequest:
    text: str
    source_lang: Optional[str]  
    target_lang: str
    fallback_lang: Optional[str]
    context: Dict = None

@dataclass
class FormattedBankingData:
    amount: str
    currency: str
    date: str
    localized_terms: Dict[str, str]
    
@dataclass
class KnowledgeGraphEntity:
    name: str
    relationships: Dict[str, List['KnowledgeGraphEntity']]

@dataclass
class Transaction:
    amount: float
    recipient: str
    currency: str
    
@dataclass
class Translation:
    text: str
    source_lang: str
    target_lang: str
    timestamp: datetime.datetime

