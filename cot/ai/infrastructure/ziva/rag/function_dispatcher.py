from typing import List, Optional

from ....domain.entities.function_calling import FunctionCallResult
from ....domain.interfaces.function_calling import IFunctionDispatcher, IFunctionCall


class FunctionDispatcher(IFunctionDispatcher):
    def __init__(
        self,
        functions: List[IFunctionCall]
    ) -> None:
        self.functions = functions
    async def dispatch_function(self,session_id: str, name: str, arguments: dict) -> Optional[FunctionCallResult]:
        for function in self.functions:
            if function.name == name:
                function.session_id = session_id
                return await function.execute(**arguments)
        return  None
