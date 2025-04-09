from typing import Dict, List, Optional

from ....domain.entities.transalation import TranslationRequest


from ..use_cases.multilingual import *


class TranslationHandler(ITranslationUseCase):
    def __init__(
        self,
        detect_lang_uc: IDetectLanguageUseCase,
        translator_uc: ITranslateUseCase,
        translate_banking_terms_uc: ITranslateBankingTermsUseCase,
        translate_amount_uc: ITranslateTextUseCase,
        find_banking_terms_uc: IFindBankingTermsUseCase,
    ) -> None:
        self.translator_uc = translator_uc
        self.detect_lang_uc = detect_lang_uc
        self.translate_amount_uc = translate_amount_uc
        self.translate_banking_terms_uc = translate_banking_terms_uc
        self.find_banking_terms_uc = find_banking_terms_uc

    def execute(
        self,
        request: TranslationRequest,
        supported_languages: List[str] = [],
        banking_terms: Dict[str, Dict[str, str]] = {},
    ) -> str:
        if not request.fallback_lang:
            raise Exception("equest.fallback_lang is required")
        if not request.source_lang:
            request.source_lang = self.detect_lang_uc.execute(
                request.text,
                supported_languages=supported_languages,
                banking_terms=banking_terms,
                fallback=request.fallback_lang,
            )

        if request.source_lang == request.target_lang:
            return request.text
        # Special handling for amounts
        translated_text = self.translate_amount_uc.execute(request.text)
        # Translate banking terms first
        detected_banking_terms = self.find_banking_terms_uc.execute(
            request.text, request.target_lang, banking_terms
        )
        translated_text = self.translate_banking_terms_uc.execute(
            request.text, detected_banking_terms, banking_terms
        )
        # Full translation if needed
        if translated_text == request.text:
            translated_text = self.translator_uc.execute(request)
        return translated_text


class UserInputHandler:
    def __init__(
        self,
        detect_language_uc: OptimizedDetectLanguageUseCase,
        find_banking_terms_uc: FindBankingTermsUseCase,
        translation_uc: ITranslationUseCase,
        supported_languages: List[Language],
        banking_terms: dict[str, dict[str, str]],
    ) -> None:
        self.detect_language_uc = detect_language_uc
        self.find_banking_terms_uc = find_banking_terms_uc
        self.translation_uc = translation_uc
        self.supported_languages = supported_languages
        self.banking_terms = banking_terms

    def execute(
        self,
        text: str,
        user_locale: str,
        banking_terms: Dict[str, Dict[str, str]],
    ) -> Dict:
        """Full multilingual processing pipeline"""
        detected_lang = self.detect_language_uc.execute(text)
        needs_translation = detected_lang != user_locale[:2]
        processed = {
            "original_text": text,
            "detected_language": detected_lang,
            "translation_required": needs_translation,
            "terms_found": self.find_banking_terms_uc.execute(text, banking_terms),
        }

        if needs_translation:
            processed["translated_text"] = self.translation_uc.execute(
                TranslationRequest(
                    text,
                    target_lang=user_locale[:2],
                    source_lang=detected_lang,
                    supported_languages=self.supported_languages,
                    banking_terms=self.banking_terms,
                )
            )

        return processed


class MultilingualController:
    def __init__(
        self,
        translation_uc: ITranslationUseCase,
        user_input_uc: IUserInputUseCase,
        supported_languages: List[Language],
        locale_settings: Dict[str, LocaleSettings],
        banking_terms: dict[str, dict[str, str]],
        fallback_lang: str,
    ):
        self.translation_uc = translation_uc
        self.user_input_uc = user_input_uc
        self.supported_languages = supported_languages
        # Locale-specific configurations
        self.locale_settings = locale_settings

        # Banking term mappings
        self.banking_terms = banking_terms

        self.fallback_lang = fallback_lang

    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
    ) -> str:
        return self.translation_uc.execute(
            request=TranslationRequest(
                text,
                fallback_lang=self.fallback_lang,
                target_lang=target_lang,
                source_lang=source_lang,
                context={},
            ),
            supported_languages=self.supported_languages,
            banking_terms=self.banking_terms,
        )

    def handle_user_input(self, text: str, user_locale: str):
        return self.user_input_uc.execute(text, user_locale, self.banking_terms)

    # for language in self.supported_languages:
