import uuid

from ..interfaces.datasource import IDatasource
from ..interfaces.async_datasource import IAsyncDatasource
from ..interfaces.ai_engine import IAIEngine, IAsyncAIEngine
from ..interfaces.genai import IGenAIAdapter, IAsyncGenAIAdapter
from .conversation import Conversation


class AIEngine(IAIEngine):
    def __init__(self,  generator:IGenAIAdapter, datasource: IDatasource) -> None :
        self.generator = generator
        self.datasource = datasource
    def init(self) -> None :
        self.datasource.init()
    def start_conversation(self, id: str) -> Conversation:
        id =  str(uuid.uuid4()) if id == "" or id is None else id.strip()
        return Conversation(
            id,
            history = [],
            entities = {}
        )
class AsyncAIEngine(IAsyncAIEngine):
    def __init__(self,  generator: IAsyncGenAIAdapter, datasource: IAsyncDatasource) -> None :
        self.generator = generator
        self.datasource = datasource
    async def init(self) -> None :
        await self.datasource.init()
    async def start_conversation(self, id: str) -> Conversation:
        id = str(uuid.uuid4()) if id == "" or id is None else id.strip()
        return Conversation(
            id,
            history = [],
            entities = {}
        )