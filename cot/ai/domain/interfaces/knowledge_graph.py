from abc import ABC, abstractmethod
from typing import Dict, List
from neo4j import Driver

class IKnowledgeGraph(ABC):
    driver: Driver  
    @abstractmethod 
    def get_related_entities(self, entity_name: str, relationship_type: str) -> List[Dict]:
        """Query connected entities in knowledge graph"""
       
    @abstractmethod
    def expand_query_context(self, query: str, entities: List[str]) -> Dict:
        """Enhance query with KG context"""
        
class IAsyncKnowledgeGraph:
    driver: Driver   
    async def get_related_entities(self, entity_name: str, relationship_type: str) -> List[Dict]:
        """Query connected entities in knowledge graph"""
       
    
    async def expand_query_context(self, query: str, entities: List[str]) -> Dict:
        """Enhance query with KG context"""