from typing import List, Optional

from .entity_extration import EntityExtrationHandler
from .multilingual import MultilingualController


class LanguageProcessor:
    def __init__(
        self,
        multilingual_controller: MultilingualController,
        entity_extration_controller: EntityExtrationHandler,
    ) -> None:
        self.multilingual_controller = multilingual_controller
        self.entity_extration_controller = entity_extration_controller

    def translate(
        self, text: str, target_lang: str, source_lang: Optional[str] = None
    ) -> str:
        return self.multilingual_controller.translate(
            text,
            target_lang=target_lang,
            source_lang=source_lang,
        )

    def handle_user_input(self, text: str, user_locale: str):
        return self.multilingual_controller.handle_user_input(
            text=text, user_locale=user_locale
        )

    def suggest_services(self, customer_name):
        self.entity_extration_controller.suggest_services(customer_name)

    def detect_fraud_patterns(self, transaction):
        self.detect_fraud_patterns(transaction)

    def handle_query(
        self,
        query: str = "What are the rules for transfers",
        entities: List[str] = ["money_transfer"],
    ):
        self.entity_extration_controller.handle_query(query, entities)
