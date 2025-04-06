from typing import Dict, List


class GetLocaleFromHeadersUseCase:
    def __init__(self,supported_languages: List[str]) -> None:
        self.supported_languages = supported_languages
    def execute (self,  headers: Dict) -> str:
        """Extract locale from HTTP headers with fallback"""
        accept_language = headers.get('Accept-Language', 'en')
        for lang in accept_language.split(','):
            code = lang.split(';')[0].strip()[:2]
            if code in self.supported_languages:
                return f"{code}_{code.upper()}"  # Simple country mapping
        return 'en_US'