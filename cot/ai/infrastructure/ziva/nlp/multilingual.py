import re
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator
from pymongo import MongoClient
from datetime import datetime
from typing import Tuple, Optional

import os
import pytz
from money import Money

class MultilingualHandler:
    def __init__(self):
        self.supported_languages = ['en', 'fr', 'es', 'pt', 'ar']
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.translation_cache = self.client.banking_rag.translation_cache
        
        # Locale-specific configurations
        self.locale_settings = {
            'en_US': {'currency': 'USD', 'timezone': 'America/New_York'},
            'en_NG': {'currency': 'NGN', 'timezone': 'Africa/Lagos'},
            'fr_FR': {'currency': 'EUR', 'timezone': 'Europe/Paris'},
            'ar_AE': {'currency': 'AED', 'timezone': 'Asia/Dubai'}
        }
        
        # Banking term mappings
        self.banking_terms = {
            'account': {'en': 'account', 'fr': 'compte', 'es': 'cuenta'},
            'transfer': {'en': 'transfer', 'fr': 'virement', 'es': 'transferencia'}
        }

    def detect_language(self, text: str, fallback: str = 'en') -> str:
        """Robust language detection with banking text optimization"""
        try:
            # Pre-check for known banking terms
            for lang in self.supported_languages:
                if any(term in text.lower() for term in self._get_banking_terms(lang)):
                    return lang
            
            # Use langdetect for general cases
            lang = detect(text)
            return lang if lang in self.supported_languages else fallback
        except LangDetectException:
            return fallback

    def translate_text(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
        """Cached translation with banking term normalization"""
        if not source_lang:
            source_lang = self.detect_language(text)
            
        if source_lang == target_lang:
            return text
            
        # Check cache first
        cache_key = f"{source_lang}_{target_lang}_{hash(text)}"
        cached = self.translation_cache.find_one({"key": cache_key})
        if cached:
            return cached["translation"]
            
        # Special handling for amounts
        amount_match = re.search(r'(\d+[\.,]?\d*)\s*([A-Z]{3})?', text)
        if amount_match:
            amount, curr = amount_match.groups()
            normalized_amount = amount.replace(',', '.')
            return text.replace(amount, normalized_amount)
            
        # Translate banking terms first
        translated_text = text
        for term in self._find_banking_terms(text):
            if term in self.banking_terms:
                translated_text = translated_text.replace(
                    term, 
                    self.banking_terms[term].get(target_lang, term))
        
        # Full translation if needed
        if translated_text == text:
            translated_text = GoogleTranslator(
                source=source_lang, 
                target=target_lang).translate(text)
            
        # Cache result
        self.translation_cache.update_one(
            {"key": cache_key},
            {"$set": {
                "translation": translated_text,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "timestamp": datetime.utcnow()
            }},
            upsert=True
        )
        
        return translated_text

    def format_banking_data(self, data: dict, locale_code: str) -> dict:
        """Locale-aware formatting for banking data"""
        locale_info = self.locale_settings.get(locale_code, self.locale_settings['en_US'])
        
        # Format currency
        if 'amount' in data:
            try:
                money = Money(data['amount'], locale_info['currency'])
                data['formatted_amount'] = money.format(locale_code)
            except:
                data['formatted_amount'] = f"{data['amount']} {locale_info['currency']}"
        
        # Format dates
        if 'date' in data:
            tz = pytz.timezone(locale_info['timezone'])
            local_date = data['date'].astimezone(tz)
            data['formatted_date'] = local_date.strftime('%x %X')
        
        # Localize banking terms
        if 'transaction_type' in data:
            data['localized_type'] = self.banking_terms.get(
                data['transaction_type'], {}).get(locale_code[:2], data['transaction_type'])
                
        return data

    def get_locale_from_headers(self, headers: dict) -> str:
        """Extract locale from HTTP headers with fallback"""
        accept_language = headers.get('Accept-Language', 'en')
        for lang in accept_language.split(','):
            code = lang.split(';')[0].strip()[:2]
            if code in self.supported_languages:
                return f"{code}_{code.upper()}"  # Simple country mapping
        return 'en_US'

    def _find_banking_terms(self, text: str) -> list:
        """Extract known banking terms from text"""
        return [term for term in self.banking_terms 
                if term.lower() in text.lower()]

    def _get_banking_terms(self, lang: str) -> list:
        """Get all banking terms for a language"""
        return [v[lang] for v in self.banking_terms.values() if lang in v]

    def handle_user_input(self, text: str, user_locale: str) -> dict:
        """Full multilingual processing pipeline"""
        detected_lang = self.detect_language(text)
        needs_translation = detected_lang != user_locale[:2]
        
        processed = {
            "original_text": text,
            "detected_language": detected_lang,
            "translation_required": needs_translation,
            "terms_found": self._find_banking_terms(text)
        }
        
        if needs_translation:
            processed["translated_text"] = self.translate_text(
                text, 
                target_lang=user_locale[:2],
                source_lang=detected_lang)
        
        return processed