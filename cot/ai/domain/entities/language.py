from typing import Optional

class Language:
    def __init__(self, language: str, code:Optional[str] = None, note:Optional[str] = None ) -> None:
        self.language = language
        self.code = code
        self.note = note