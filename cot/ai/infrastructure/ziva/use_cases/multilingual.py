# use_cases/multilingual.py
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
        request.context = {
            "banking_terms": self.repo.get_localized_terms(request.target_lang)
        }
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
