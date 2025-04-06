from typing import Dict, List
from ....domain.interfaces.knowledge_graph import IKnowledgeGraph

class CheckTransferRegulationsUseCase:
    def __init__(self, knowledge_graph: IKnowledgeGraph):
        self.kg = knowledge_graph

    def execute(self) -> Dict[str, List[str]]:
        context = self.kg.expand_query_context(
            "What are the rules for transfers?", 
            ["money_transfer"]
        )
        return {
            "regulations": [
                r["name"] for r in 
                context["money_transfer"]["regulations"]
            ]
        }