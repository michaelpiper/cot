from typing import Dict, List, Optional

from ....domain.entities.transalation import TranslationRequest


from ..use_cases.multilingual import *


class TranslationHandler:
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
        text: str,
        fallback_lang: str,
        target_lang: str,
        source_lang: Optional[str] = None,
        supported_languages: List[str] = [],
        banking_terms: Dict[str, Dict[str, str]] = {},
    ) -> str:
        if not source_lang:
            source_lang = self.detect_lang_uc.execute(
                text,
                supported_languages=supported_languages,
                banking_terms=banking_terms,
                fallback=fallback_lang,
            )

        if source_lang == target_lang:
            return text
        # Special handling for amounts
        translated_text = self.translate_amount_uc.execute(text)
        # Translate banking terms first
        detected_banking_terms = self.find_banking_terms_uc.execute(
            text, target_lang, banking_terms
        )
        translated_text = self.translate_banking_terms_uc.execute(
            text, detected_banking_terms, banking_terms
        )
        # Full translation if needed
        if translated_text == text:
            translated_text = self.translator_uc.execute(
                TranslationRequest(
                    text=text,
                    source_lang=source_lang,
                    target_lang=target_lang,
                )
            )
        return translated_text


class UserInputHandler:
    def __init__(
        self,
        detect_language_uc: OptimizedDetectLanguageUseCase,
        find_banking_terms_uc: FindBankingTermsUseCase,
        translate_uc: CacheOrTranslateUseCase,
    ) -> None:
        self.detect_language_uc = detect_language_uc
        self.find_banking_terms_uc = find_banking_terms_uc
        self.translate_uc = translate_uc

    def execute(
        self, text: str, user_locale: str, banking_terms: Dict[str, Dict[str, str]]
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
            processed["translated_text"] = self.translate_uc.execute(
                TranslationRequest(
                    text,
                    target_lang=user_locale[:2],
                    source_lang=detected_lang,
                )
            )

        return processed


class MultilingualHandler:
    def __init__(
        self,
        translator_handler: TranslationHandler,
        user_input_handler: UserInputHandler,
    ):
        self.translator_handler = translator_handler
        self.user_input_handler = user_input_handler
        self.supported_languages = ["en", "fr", "es", "pt", "ar"]
        # Locale-specific configurations
        self.locale_settings = {
            "en_US": {"currency": "USD", "timezone": "America/New_York"},
            "en_NG": {"currency": "NGN", "timezone": "Africa/Lagos"},
            "fr_FR": {"currency": "EUR", "timezone": "Europe/Paris"},
            "ar_AE": {"currency": "AED", "timezone": "Asia/Dubai"},
        }

        # Banking term mappings
        self.banking_terms = {
            "account": {"en": "account", "fr": "compte", "es": "cuenta"},
            "transfer": {"en": "transfer", "fr": "virement", "es": "transferencia"},
        }

        self.fallback_lang = "en"

    def translate(
        self, text: str, target_lang: str, source_lang: Optional[str] = None
    ) -> str:
        return self.translator_handler.execute(
            text,
            fallback_lang=self.fallback_lang,
            target_lang=target_lang,
            source_lang=source_lang,
            supported_languages=self.supported_languages,
            banking_terms=self.banking_terms,
            
        )

    def handle_user_input(self, text: str, user_locale: str):
        return self.user_input_handler.execute(text, user_locale, self.banking_terms)

    # for language in self.supported_languages:
