from ....domain.interfaces import IKnowledgeGraph
from ....domain.entities import Transaction

class DetectFraudPatternUseCase:
    def __init__(self, knowledge_graph: IKnowledgeGraph):
        self.kg = knowledge_graph

    def execute(self, transaction: Transaction) -> bool:
        """
        Example transaction:
        {"amount": 10000, "recipient": "KFC", "currency": "USD"}
        
        Returns:
        [
            {"name": "money_transfer", "relationship": "USED_BY", "confidence": null}
        ]
        """
        related = self.kg.get_related_entities(
            transaction.recipient, 
            "USED_BY"
        )
        return any(rel["name"] == "money_transfer" for rel in related)
