# use_cases/multilingual.py
from datetime import datetime, timezone
import re
from typing import Dict, List
from ....domain.entities import *
from ....domain.interfaces import *


class DetectLanguageUseCase:
    def __init__(self, detector: ILanguageDetector):
        self.detector = detector

    def execute(self, text: str) -> str:
        return self.detector.detect(text)


class HandleTranslationUseCase:
    def __init__(self, translator: ITranslator, repository: ILocalizationRepository):
        self.translator = translator
        self.repo = repository

    def execute(self, request: TranslationRequest) -> str:
        # Add banking-specific terms to context
        request.context.update(
            {"banking_terms": self.repo.get_localized_terms(request.target_lang)}
        )
        return self.translator.translate(request)


class AsyncDetectLanguageUseCase:
    def __init__(self, detector: IAsyncLanguageDetector):
        self.detector = detector

    async def execute(self, text: str) -> str:
        return await self.detector.detect(text)


class AsyncHandleTranslationUseCase:
    def __init__(
        self, translator: IAsyncTranslator, repository: IAsyncLocalizationRepository
    ):
        self.translator = translator
        self.repo = repository

    async def execute(self, request: TranslationRequest) -> str:
        request.context.update(
            {"banking_terms": await self.repo.get_localized_terms(request.target_lang)}
        )
        return await self.translator.translate(request)


class OptimizedDetectLanguageUseCase(IDetectLanguageUseCase):
    def __init__(self, detector: ILanguageDetector) -> None:
        self.detector = detector

    def _get_banking_terms(
        self, lang: str, banking_terms: Dict[str, Dict[str, str]]
    ) -> list:
        """Get all banking terms for a language"""
        return [v[lang] for v in banking_terms.values() if lang in v]

    def execute(
        self,
        text: str,
        supported_languages: List[str],
        banking_terms: Dict = {},
        fallback: str = "en",
    ) -> str:
        """Robust language detection with banking text optimization"""
        try:
            # Pre-check for known banking terms
            for lang in supported_languages:
                if any(
                    term in text.lower()
                    for term in self._get_banking_terms(lang, banking_terms)
                ):
                    return lang

            # Use langdetect for general cases
            lang = self.detector.detect(text)
            return lang if lang in supported_languages else fallback
        except:
            return fallback


class TranslateBankingTermsUseCase(ITranslateBankingTermsUseCase):

    def execute(
        self,
        text: str,
        target_lang: str,
        detected_banking_terms: list[str],
        banking_terms: Dict[str, Dict[str, str]],
    ):
        translated_text = text
        for term in detected_banking_terms:
            if term in banking_terms:
                translated_text = translated_text.replace(
                    term, banking_terms[term].get(target_lang, term)
                )
        return translated_text


class TranslateSpecialHandlingForAmountUseCase(ITranslateTextUseCase):
    def __init__(self) -> None: ...

    def execute(self, text: str) -> str:
        amount_match = re.search(r"(\d+[\.,]?\d*)\s*([A-Z]{3})?", text)
        if amount_match:
            amount, curr = amount_match.groups()
            normalized_amount = amount.replace(",", ".")
            return text.replace(amount, normalized_amount)


class TranslateUseCase(ITranslateUseCase):
    def __init__(
        self, repository: ILocalizationRepository, translator: ITranslator
    ) -> None:
        self.repo = repository
        self.translator = translator

    def execute(self, request: TranslationRequest) -> str:
        return self.translator.translate(request)


class CacheOrTranslateUseCase(ITranslateUseCase):
    def __init__(self, repository: ITranslationCache, translator: ITranslator) -> None:
        self.repo = repository
        self.translator = translator

    def execute(self, request: TranslationRequest) -> str:
        """Cached translation with banking term normalization"""
        # Check cache first
        cache_key = f"{request.source_lang}_{request.target_lang}_{hash(request.text)}"
        cached = self.repo.get(cache_key)
        if cached:
            return cached.text

        translated_text = self.translator.translate(request)

        # Cache result
        self.repo.set(
            cache_key,
            Translation(
                text=request.text,
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                timestamp=datetime.now(timezone.utc),
            ),
        )

        return translated_text


class FindBankingTermsUseCase(IFindBankingTermsUseCase):
    def __init__(self) -> None: ...

    def execute(self, text: str, banking_terms: Dict[str, Dict[str, str]]) -> list:
        """Extract known banking terms from text"""
        return [term for term in banking_terms if term.lower() in text.lower()]
