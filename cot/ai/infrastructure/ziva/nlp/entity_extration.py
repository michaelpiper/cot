from ..rag.knowledge_graph import IKnowledgeGraph
class EntityExtrationHandler:
    def __init__( self, kg: IKnowledgeGraph) -> None:
        self.kg = kg
    # Scenario 1: Customer asks about transfer regulations
    def handle_query(self, query: str = "What are the rules for transfers?", entities = ["money_transfer"]) -> None:
        context = self.kg.expand_query_context( query, entities)
        
        """
        Returns:
        {
            "money_transfer": {
                "related_services": [],
                "regulations": [
                    {"name": "PSD2", "relationship": "GOVERNED_BY", "confidence": null}
                ]
            }
        }
        """
        regulations ={}
        for entity in entities:
            regulations[entity] =  context[entity].get("regulations")
            print(f"ℹ️ Transfers are governed by: {', '.join([r['name'] for r in regulations[entity]])}")
            # Output: ℹ️ Transfers are governed by: PSD2

        return regulations
        # if regulations:
    
    # Scenario 2: Fraud detection pattern
    def detect_fraud_patterns(self,transaction):
        related = self.kg.get_related_entities(transaction["recipient"], "USED_BY")
        
        """
        Example transaction:
        {"amount": 10000, "recipient": "KFC", "currency": "USD"}
        
        Returns:
        [
            {"name": "money_transfer", "relationship": "USED_BY", "confidence": null}
        ]
        """
        
        if any(rel["name"] == "money_transfer" for rel in related):
            print(f"⚠️ Abnormal transaction pattern detected with {transaction['recipient']}")
            # Output: ⚠️ Abnormal transaction pattern detected with KFC

    # Scenario 3: Cross-selling opportunities
    def suggest_services(self,customer_name):
        services = self.kg.get_related_entities(customer_name, "USED_BY")
        
        """
        For customer "John Doe", returns:
        [
            {"name": "personal_loan", "relationship": "USED_BY", "confidence": null}
        ]
        """
        
        if services:
            print(f"💡 Customer might benefit from: {services[0]['name']}")
            # Output: 💡 Customer might benefit from: personal_loan