from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from ..entities.function_calling import FunctionCallResult
class IFunctionCall(ABC):
    name: str
    description: str
    context: Optional[str]
    parameters: Dict
    session_id: Optional[str]
    @property
    def    __name__(self):
        return self.name
    @property
    def __dict__(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
    async def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)
    @abstractmethod
    async def execute(self, *args, **kwargs)-> FunctionCallResult:...
    
class IFunctionDispatcher:
    functions: List[IFunctionCall]
  
    @abstractmethod
    async def dispatch_function(self, session_id: str, name: str, arguments: dict) -> Optional[FunctionCallResult]:...
