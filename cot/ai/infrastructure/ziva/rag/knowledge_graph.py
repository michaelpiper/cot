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
        """Enhance query with KG context and potentially modify the query"""
        context = {
            "_original_query": query  # Store the original query without modification
        }
        
        # Expand context by fetching related entities for each provided entity
        for entity in entities:
            related_services = self.get_related_entities(entity, "HAS_SERVICE")
            regulations = self.get_related_entities(entity, "GOVERNED_BY")
            
            # Store the retrieved context
            context[entity] = {
                "related_services": related_services,
                "regulations": regulations
            }
            
            # Dynamically enhance the query with additional information based on context
            if related_services:
                query += f" AND e.name IN {', '.join([service['name'] for service in related_services])}"
            if regulations:
                query += f" AND e.name IN {', '.join([reg['name'] for reg in regulations])}"
        
        #return the modified query here if it was enhanced
        context["_query"] = query
        return context