from abc import abstractmethod
from ..models.entity import Entity
from .repository import *
from .async_repository import *
class IEntityRepository[Conn](IRepository[Conn], IFindOneByIdRepository[Entity]):
    @abstractmethod
    def update_or_create_by_conversation_id_and_key(self, conversationId: str, key: str, value: Union[str]) -> None:...
       
    @abstractmethod    
    def find_one_by_conversation_id_and_key(self, conversationId: str, key: Union[str, object]) -> Union[Entity, None]:...
       
    @abstractmethod 
    def find_many_by_conversation_id(self, conversationId: str) -> List[Entity]:...
    
    @abstractmethod   
    def get_one_by_conversation_id_and_key(self, conversationId: str, key: Union[str, object]) -> Union[Entity, None]:...
    
    @abstractmethod
    def get_all_by_conversation_id(self, conversationId: str) -> List[Entity]:...
        
class IAsyncEntityRepository[Conn]( IAsyncRepository[Conn], IFindOneByIdRepository[Entity]):
    @abstractmethod
    async def update_or_create_by_conversation_id_and_key(self, conversationId: str, key: str, value: Union[str]) -> None:...
       
    @abstractmethod    
    async def find_one_by_conversation_id_and_key(self, conversationId: str, key: Union[str, object]) -> Union[Entity, None]:...
       
    @abstractmethod 
    async def find_many_by_conversation_id(self, conversationId: str) -> List[Entity]:...
    
    @abstractmethod   
    async def get_one_by_conversation_id_and_key(self, conversationId: str, key: Union[str, object]) -> Union[Entity, None]:...
    
    @abstractmethod
    async def get_all_by_conversation_id(self, conversationId: str) -> List[Entity]:...
        