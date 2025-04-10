from ....domain.interfaces.session_repository import ISessionManager
from ....domain.entities.function_calling import FunctionCallResult
from ....domain.interfaces.function_calling import IFunctionCall


class CheckAuthUseCase(IFunctionCall):
    name = "check_auth"
    description = "Check the session auth status."
    parameters = {
        "type": "object",
        "properties": {
        },
        "required": [],
    }
    
    def __init__(self, session_manager:ISessionManager):
        self.session_manager = session_manager

    async def execute(self):
        return await self.check_auth()

    async def check_auth(self) -> FunctionCallResult:
        session = await self.session_manager.get(session_id=self.session_id)
            
       
        return FunctionCallResult(
            f"",
           next_step= f"Auth Status -> {"unauthenticated" if not session.get('auth.access_token')else "authenticated -> continue action"}\n.",
        )
