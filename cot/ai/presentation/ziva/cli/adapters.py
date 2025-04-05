# presentation/cli/adapters.py
from typing import List
class ZiVACLIPresenter:
    @staticmethod
    def show_regulations(regulations: List[str]):
        if regulations:
            print(f"ℹ️ Transfers are governed by: {', '.join(regulations)}")

    @staticmethod
    def show_fraud_alert(recipient: str):
        print(f"⚠️ Abnormal transaction pattern detected with {recipient}")

    @staticmethod
    def show_service_suggestion(service: str):
        print(f"💡 Customer might benefit from: {service}")