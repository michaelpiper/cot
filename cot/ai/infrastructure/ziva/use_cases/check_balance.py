from ....core.logger import logger
from ....domain.interfaces.session_repository import ISessionManager
from ....domain.entities.function_calling import FunctionCallResult
from ....domain.interfaces.function_calling import IFunctionCall


class CheckAccountBalanceUseCase(IFunctionCall):
    name = "check_account_balance"
    description = "Check the account balance."
    parameters = {
        "type": "object",
        "properties": {
            "account_type": {"type": "string", "enum": ["savings", "current"]}
        },
        "required": ["account_type"],
    }

    def __init__(self, session_manager: ISessionManager):
        self.session_manager = session_manager

    async def execute(self, account_type: str = None):
        return await self.check_balance(account_type)

    async def check_balance(self, account_type: str = None) -> FunctionCallResult:
        session = await self.session_manager.get(session_id=self.session_id)
        logger.info("session: {}".format(session))
        if not session.get("auth.access_token"):
            session.set('intent', 'check_account_balance')
            await  self.session_manager.save(session)
            return FunctionCallResult(
               f"Check Balance -> requires authenticate function call -> ask user to provide phone number you would be sent an otp for authentication",
            )

        balances = {"savings": 20500.75, "current": 12000.00}
        return FunctionCallResult(
            f"Your {account_type} account balance is ₦{balances.get(account_type.lower(), 0):,.2f}.",
            # context=f"Account Type -> {account_type}\nAccount Balance -> ₦{balances.get(account_type.lower(), 0):,.2f}.",
        )
