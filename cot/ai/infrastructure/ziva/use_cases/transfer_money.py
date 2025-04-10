from cot.ai.domain.interfaces.session_repository import ISessionManager
from ....domain.entities.function_calling import FunctionCallResult
from ....domain.interfaces.function_calling import IFunctionCall


class TransferMoneyUseCase(IFunctionCall):
    name = "transfer_money"
    description = "Transfer funds to a recipient."
    parameters = {
        "type": "object",
        "properties": {"amount": {"type": "number"}, "recipient": {"type": "string"}},
        "required": ["amount", "recipient"],
    }
    def __init__(self, session_manager:ISessionManager):
        self.session_manager = session_manager
    async def execute(self, amount: float=None, recipient: str =None):
        return await self.transfer_money(amount, recipient)
    async def transfer_money(self, amount: float=None, recipient: str =None) -> FunctionCallResult:
        if amount is None:
            return FunctionCallResult(f"Ask Question -> provide amount")
        if recipient is None:
            return FunctionCallResult(f"Ask Question -> provide recipient")
        return FunctionCallResult(f"₦{amount:,.2f} has been sent to {recipient}.")
