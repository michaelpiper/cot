from typing import List, Optional

from ....domain.interfaces.function_calling import IFunctionCall
from ....domain.interfaces import IAsyncGenAIAdapter
from ....domain.models import ChatPrompt
from google import genai
from google.genai import types


class GemmaGenAIAdapter(IAsyncGenAIAdapter):
    DEFAULT_MODEL = "gemini-2.0-flash"

    def __init__(self, api_key: str, model: str = None) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model if model else GemmaGenAIAdapter.DEFAULT_MODEL

    async def generate(
        self,
        prompt,
        max_new_tokens=50,
        truncation=False,
        num_return_sequences=1,
        temperature=0.7,
        function_tools: Optional[List[IFunctionCall]] = None,
    ):
        prompt = (
            ChatPrompt.from_str(prompt)
            if isinstance(prompt, str)
            else ChatPrompt(prompt)
        )
        chat_config = types.GenerateContentConfig(
            system_instruction=prompt.get_system_content(),
            temperature=temperature,
            max_output_tokens=max_new_tokens,
            tools=[],
            tool_config=types.ToolConfig(),
        )
        if function_tools:
            tools: List[IFunctionCall] = []
            for function_tool in function_tools:
                
                try:
                    print("{} {}".format(function_tool.__name__, function_tool()))
                except Exception as e:
                    print("{} err: {}".format(function_tool.__name__, e))
                tools.append(types.ToolCodeExecution(function_tool))
            tools.append(
                types.Tool(function_declarations=[tool.__dict__ for tool in tools])
            )
            chat_config.tools = tools

        chat = self.client.models.generate_content_stream(
            model=self.model,
            contents=prompt.get_last_user_content(),
            config=chat_config,
        )
        response = ""
        for output in chat:
            response += output.text
        return response
