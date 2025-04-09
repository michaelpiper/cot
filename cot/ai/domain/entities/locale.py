from typing import Optional


class Locale:
    def __init__(self, code: str):
        self.code = code
        self.language, self.country = self._parse_code()
    
    def _parse_code(self) -> tuple:
        parts = self.code.split('_')
        return (parts[0], parts[1]) if len(parts) > 1 else (parts[0], None)
    
class Currency:
    def __init__(self, code: str, symbol: Optional[str] = None, name: Optional[str] = None) -> None:
        self.code = code  
        
        self.symbol = symbol
        
        self.name = name
class LocaleSettings:
    def __init__(self, locale:Locale, currency: Currency, timezone: str) -> None:
        self.locale = locale
        self.currency =  currency
        self.timezone=timezone