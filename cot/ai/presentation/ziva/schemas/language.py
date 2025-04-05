# presentation/language/schemas.py
from pydantic import BaseModel

class LanguageDetectionResponse(BaseModel):
    original_text: str
    detected_language: str
    needs_translation: bool

class TranslationResponse(LanguageDetectionResponse):
    translated_text: str