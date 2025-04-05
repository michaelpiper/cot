# adapters/external/langdetect_adapter.py
from .....domain.interfaces.genai import IAsyncGenAIAdapter
from .....domain.models.chat_prompt import ChatPrompt

from .....domain.interfaces import IAsyncLanguageDetector




class AsyncZiVALangDetectAdapter(IAsyncLanguageDetector):
    def __init__(self, gen_ai: IAsyncGenAIAdapter):
        self.gen_ai = gen_ai
    async def get_system_prompt(self):
        return """
        ---

        ### **System Prompt:**  
        *"Detect the language of the user's input strictly from this list:*  
        - **Nigeria Pidgin** → `pcm` *(ISO 639-3, no ISO 639-1 exists)*  
        - **Yoruba** → `yo`  
        - **English** → `en`  
        - **French** → `fr`  
        - **Arabic** → `ar`  
        - **Hindi (India)** → `hi`  

        *If the input does not match any of these, default to `en`. Respond ONLY with the correct code—no explanations."*  

        ---

        ### **Key Features:**  
        ✅ **Restricted Detection**: Only checks for the 6 specified languages.  
        ✅ **Handles Pidgin**: Uses `pcm` (ISO 639-3) since Nigeria Pidgin lacks an ISO 639-1 code.  
        ✅ **Fallback**: Defaults to `en` for unrecognized inputs.  
        ✅ **No Extra Text**: Outputs **only** the code (e.g., `yo`, `fr`, `hi`).  

        ### **Example Outputs:**  
        - *"How far?"* → `pcm` (Nigeria Pidgin)  
        - *"Ṣe daadạ ni?"* → `yo` (Yoruba)  
        - *"Hello"* → `en`  
        - *"नमस्ते"* → `hi` (Hindi)  
        - *"Unknown text 123"* → `en` (fallback)  
        """
    async def detect(self, text: str) -> str:
        # Wrap sync lib in async executor
        prompt = ChatPrompt()
        prompt.add_system_content(await self.get_system_prompt())
        prompt.add_user_content(text)
        lang = await self.gen_ai.generate(
            prompt,
            max_new_tokens=3
        )
        if isinstance(lang, str):
            return lang.strip()
        
        a_lang= ''
        for chunk in lang:
            a_lang += chunk
        return a_lang.strip()