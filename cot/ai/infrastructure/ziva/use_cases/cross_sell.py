from typing import Optional

from ....domain.interfaces import IKnowledgeGraph


class SuggestServicesUseCase:
    def __init__(self, knowledge_graph: IKnowledgeGraph):
        self.kg = knowledge_graph

    def execute(self, customer_name: str) -> Optional[str]:
        services = self.kg.get_related_entities(customer_name, "USED_BY")
        return services[0]["name"] if services else None
