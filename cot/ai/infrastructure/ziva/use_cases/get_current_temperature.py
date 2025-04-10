from cot.ai.domain.interfaces.session_repository import ISessionManager
from ....domain.entities.function_calling import FunctionCallResult
from ....domain.interfaces.function_calling import IFunctionCall


class GetCurrentTemperatureUseCase(IFunctionCall):
    """Gets the current temperature for a given location.
        Args:
            location: The city and state, e.g. San Francisco, CA

        Returns:
            A dictionary containing the temperature and unit.
    """
    name = "get_current_temperature"
    description = "get current temperature."
    parameters = {
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"],
    }
    def __init__(self, session_manager:ISessionManager):
        self.session_manager = session_manager
    def execute(self, location: str):
        return self.get_current_temperature(location)
    # Define the function with type hints and docstring
    
    def get_current_temperature(self,location: str) -> dict:
        # ... (implementation) ...
        return  FunctionCallResult(f"temperature 25 unit Celsius")