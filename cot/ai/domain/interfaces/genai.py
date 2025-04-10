from abc import abstractmethod
from typing import Dict, List, Optional, Union, Generator

from ...domain.interfaces.function_calling import IFunctionCall


class IGenAIAdapter:
    @abstractmethod
    def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]], 
        max_new_tokens=50,
        truncation=False,
        num_return_sequences=1,
        temperature=0.7,
        function_tools: Optional[List[IFunctionCall]] = None,
    ) -> Union[str,Generator[str, str, str]]:...

class IAsyncGenAIAdapter:
    @abstractmethod
    async def generate(
        self,
        prompt: Union[str, List[Dict[str, str]]], 
        max_new_tokens=50,
        truncation=False,
        num_return_sequences=1,
        temperature=0.7,
        function_tools: Optional[List[IFunctionCall]] = None,
    ) -> Union[str,Generator[str, str, str]]:...