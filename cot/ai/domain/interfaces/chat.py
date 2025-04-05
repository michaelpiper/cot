from abc import abstractmethod
from ..models.chat import Chat
from .repository import *
from .async_repository import *
class IChatRepository[Conn](IRepository[Conn],ICreateRepository[Chat], IFindManyRepository[Chat]):
    @abstractmethod
    def find_many_by_conversation_id(self, conversationId: str)-> List[Chat]:...  
    
class IAsyncChatRepository[Conn](IAsyncRepository[Conn],IAsyncCreateRepository[Chat], IAsyncFindManyRepository[Chat]):
    @abstractmethod
    async def find_many_by_conversation_id(self, conversationId: str)-> List[Chat]:... 