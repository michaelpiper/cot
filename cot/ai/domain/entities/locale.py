class Locale:
    def __init__(self, code: str):
        self.code = code
        self.language, self.country = self._parse_code()
    
    def _parse_code(self) -> tuple:
        parts = self.code.split('_')
        return (parts[0], parts[1]) if len(parts) > 1 else (parts[0], None)