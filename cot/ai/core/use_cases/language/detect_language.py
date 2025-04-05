from typing import Dict, List
from ....domain.interfaces import ILanguageDetector

class DetectLanguageUseCase:
    def __init__(self, detector: ILanguageDetector, banking_terms: Dict[str, List[str]]):
        self.detector = detector
        self.banking_terms = banking_terms

    def execute(self, text: str) -> str:
        # First check for known banking terms
        for lang, terms in self.banking_terms.items():
            if any(term.lower() in text.lower() for term in terms):
                return lang
        # Fall back to detector
        return self.detector.detect(text)
