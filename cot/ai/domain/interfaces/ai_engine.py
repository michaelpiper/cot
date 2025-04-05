from typing import Any, Dict, List, Self

from .genai import IAsyncGenAIAdapter, IGenAIAdapter
from .datasource import IDatasource
from .async_datasource import IAsyncDatasource
from ..models.chat import Chat
from ..models.chat_bubble import ChatBubble
from ..models.conversation import Conversation

class IAIEngine:
    generator: IGenAIAdapter
    datasource: IDatasource
    def init(self)-> None:...
    def generate_bubbles(user_input:List[Any], entities: dict = {} ) -> List[ChatBubble]:
        pass
    
    # Function to extract entities from user input
    def extract_entities(self, user_input: List[Any] ) -> Dict:
        pass
      # Function to generate text
    def generate_text(self, user_input : List[Any], entities: dict = {}) -> str:
        pass
    
    # Function to handle conversation
    def handle_conversation(self, conversation: Conversation) -> Chat:
        pass
    
    def send_message(self, message: str, conversation: Conversation) -> Chat:
        pass
    def start_conversation(self, id: str) -> Self:
        pass
    
class IAsyncAIEngine:
    generator: IAsyncGenAIAdapter
    datasource: IAsyncDatasource
    async def init(self) -> None:...
    async def generate_bubbles(user_input:List[Any], entities: dict = {} ) -> List[ChatBubble]:
        pass
    
    # Function to extract entities from user input
    async def extract_entities(self, user_input: List[Any] ) -> Dict:
        pass
      # Function to generate text
    async def generate_text(self, user_input : List[Any], entities: dict = {}) -> str:
        pass
    
    # Function to handle conversation
    async def handle_conversation(self, conversation: Conversation) -> Chat:
        pass
    
    async def send_message(self, message: str, conversation: Conversation) -> Chat:
        pass
    async def start_conversation(self, id: str) -> Self:
        pass
