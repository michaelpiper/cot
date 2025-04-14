from cot.ai.domain.interfaces.session_repository import ISessionManager
from ....domain.entities.function_calling import FunctionCallResult
from ....domain.interfaces.function_calling import IFunctionCall
from pydantic import BaseModel, Field, field_validator
import re


class AuthenticationRequest(BaseModel):
    """Request model for user authentication"""

    phone_number: str = Field(
        description="11-digit phone number without country code",
        example="08012345678",
        pattern=r"^[0-9]{11}$",
    )
    otp: str = Field(
        description="6-digit one-time password", example="123456", pattern=r"^[0-9]{6}$"
    )

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        if not re.match(r"^[0-9]{11}$", v):
            raise ValueError("Phone number must be 11 digits")
        return v

    @field_validator("otp")
    def validate_otp(cls, v):
        if not re.match(r"^[0-9]{6}$", v):
            raise ValueError("OTP must be 6 digits")
        return v


class AuthenticateUseCase(IFunctionCall):
    """User authentication use case with phone number and OTP verification"""

    name = "authenticate"
    description = (
        "Authenticates a user using their phone number and one-time password (OTP)."
    )
    parameters = {
        "type": "object",
        "properties": {
            "phone_number": {
                "type": "string",
                "description": "11-digit Nigerian phone number without country code",
                "pattern": "^[0-9]{11}$",
            },
            "otp": {
                "type": "string",
                "description": "6-digit one-time password",
                "pattern": "^[0-9]{6}$",
            },
        },
        "required": ["phone_number", "otp"],  # Explicit required fields in JSON schema
        "additionalProperties": False,  # Prevent extra fields
    }

    def __init__(self, session_manager: ISessionManager):
        self.session_manager = session_manager

    def execute(self, phone_number: str = None, otp: str = None):
        return self.authenticate(phone_number, otp)

    async def authenticate(
        self, phone_number: str = None, otp: str = None
    ) -> FunctionCallResult:
        session = await self.session_manager.get(session_id=self.session_id)
        if phone_number is None:
            return FunctionCallResult("Ask Question -> provide phone number")
        if otp is None:
            return FunctionCallResult(
                f"Ask Question -> provide otp sent to your phone number {phone_number}"
            )
        if otp == "123445" and phone_number is not None:
            session.set("auth.access_token", "testtoken", create_missing=True)
            await self.session_manager.save(session)
        else:
            return FunctionCallResult(
                f"Ask Question -> provide valid otp sent to your phone number {phone_number}"
            )
        return FunctionCallResult(
            next_step=f"Auth Status -> unauthenticated" 
if not session.get('auth.access_token')
else f"""
Auth Status -> authenticated -> continue action -> function call: {session.get('intent', 'informational')}\n\n
## Context:
- The user has successfully authenticated.
- The previous intent detected was to check the {session.get('intent', 'informational')}.
- Now that authentication is complete, proceed with the action related to the detected intent.

## Instructions:
1. Confirm that authentication has been completed.
2. Retrieve the {session.get('intent', 'informational')}.
3. Provide the {session.get('intent', 'informational')} to the user in a clear and concise format.
4. Do **not** call the `authenticate` function again.
5. Proceed directly to call the appropriate function for the previously detected function call: 
""")
