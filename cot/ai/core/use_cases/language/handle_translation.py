from datetime import datetime
from typing import Optional
from ....domain.interfaces import ITranslator, ITranslationCache
import hashlib

from ....domain.entities.transalation import Translation

class HandleTranslationUseCase:
    def __init__(self, translator: ITranslator, cache: ITranslationCache):
        self.translator = translator
        self.cache = cache

    def execute(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
        cache_key = self._generate_cache_key(text, target_lang, source_lang)
        if cached := self.cache.get(cache_key):
            return cached.text
        
        translated = self.translator.translate(text, target_lang, source_lang)
        self.cache.set(cache_key, Translation(
            text=translated,
            source_lang=source_lang,
            target_lang=target_lang,
            timestamp=datetime.utcnow()
        ))
        return translated

    def _generate_cache_key(self, text: str, target_lang: str, source_lang: Optional[str]) -> str:
        return hashlib.md5(f"{source_lang}_{target_lang}_{text}".encode()).hexdigest()