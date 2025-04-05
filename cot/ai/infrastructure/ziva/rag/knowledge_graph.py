from typing import Dict, List
from neo4j import GraphDatabase
import os
from ....domain.interfaces import IKnowledgeGraph

class ZiVAKnowledgeGraph(IKnowledgeGraph):
    def __init__(self):
        self.driver = GraphDatabase.driver(os.getenv("NEO4J_URI"),auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD")))
    
    def get_related_entities(self, entity_name: str, relationship_type: str) -> List[Dict]:
        """Query connected entities in knowledge graph"""
        query = """
        MATCH (e:BankingEntity {name: $entity_name})
        -[r:%s]->(related)
        RETURN related.name as name, type(r) as relationship, r.weight as confidence
        """ % relationship_type
        
        with self.driver.session() as session:
            result = session.run(query, entity_name=entity_name)
            return [dict(record) for record in result]
    
    def expand_query_context(self, query: str, entities: List[str]) -> Dict:
        """Enhance query with KG context"""
        context = {}
        for entity in entities:
            context[entity] = {
                "related_services": self.get_related_entities(entity, "HAS_SERVICE"),
                "regulations": self.get_related_entities(entity, "GOVERNED_BY")
            }
        return context