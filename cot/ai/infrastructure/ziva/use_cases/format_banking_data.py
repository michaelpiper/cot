from typing import Dict
import pytz
from money import Money
class FormatBankingDataUseCase:
    def __init__(self, locale_settings:Dict[str, Dict[str, str]], banking_terms: Dict[str, Dict[str, str]] = {} ) -> None:
        self.locale_settings = locale_settings
        self.banking_terms = banking_terms
    def execute(self, data: dict, locale_code: str) -> dict:
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