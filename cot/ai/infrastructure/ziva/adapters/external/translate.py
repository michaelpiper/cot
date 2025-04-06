# adapters/external/google_translate.py
import json
from .....domain.models.chat_prompt import ChatPrompt
from .....core.logger import logger
from .....domain.entities.transalation import TranslationRequest
from .....domain.interfaces.genai import IAsyncGenAIAdapter
from .....domain.interfaces.multilingual import IAsyncTranslator




class AsyncZivaTranslateAdapter(IAsyncTranslator):
    def __init__(self, gen_ai: IAsyncGenAIAdapter):
        self.gen_ai = gen_ai
    async def get_system_prompt(self):
        return """
            ---

            ### **System Prompt:**  
            *"You are a precise translation engine. Follow these rules:*  

            1. **Input Format**:  
            ```json  
            {  
                "text": "Text to translate",  
                "source_lang": "auto|en|fr|yo|pcm|ar|hi",  // Optional (auto-detect if empty)  
                "target_lang": "en|fr|yo|pcm|ar|hi",       // Required  
                "context": {"style": "formal|casual|slang", "domain": "chat|legal|tech"} // Optional hints  
            }  
            ```  

            2. **Output**:  
            - **ONLY** the translated text, *strictly preserving* original formatting (e.g., line breaks, bold/italics).  
            - **NO** explanations, disclaimers, or metadata.  

            3. **Defaults**:  
            - If `source_lang` is missing, auto-detect (but only from allowed languages).  
            - If context hints are provided (e.g., `"slang"`), adapt tone accordingly.  

            *Example Input:*  
            ```json  
            {"text": "How far?", "target_lang": "fr", "context": {"style": "slang"}}  
            ```  
            *Example Output:*  
            `Ça va ?`  

            ---  

            ### **Key Features:**  
            ✅ **Structured Input**: Uses JSON to enforce schema.  
            ✅ **Style-Aware**: Respects `context` hints (e.g., slang → "Wassup?" vs. formal → "How are you?").  
            ✅ **No Noise**: Outputs **only** the translated text, formatted identically to input.  
            ✅ **Controlled Languages**: Only translates between specified languages (`en/fr/yo/pcm/ar/hi`).  

            ### **Edge Cases:**  
            - Untranslatable text (e.g., emoji `🌍` → returns as-is).  
            - Missing `target_lang` → **silently fails** (or you could add `"error": "MISSING_TARGET_LANG"` if needed).  
            """
    async def translate(self, request: TranslationRequest) -> str:
         # Wrap sync lib in async executor
        prompt = ChatPrompt()
        prompt.add_system_content(await self.get_system_prompt())
        prompt.add_user_content(json.dumps({
             "text": request.text,
            "target_lang": request.target_lang,
            "source_lang": request.source_lang,
            "context": request.context 
        }))
        translation = await self.gen_ai.generate(
            prompt,
            max_new_tokens=500
        )
        if isinstance(translation, str):
            logger.info("translate json response %s %s",  {
                "q": request.text,
                "target": request.target_lang,
                "source": request.source_lang,
                "context": request.context
            }, translation)
            return translation.strip()
        
        a_translation= ''
        for chunk in translation:
            a_translation += chunk
        logger.info("translate json response %s %s",  {
                "q": request.text,
                "target": request.target_lang,
                "source": request.source_lang,
                "context": request.context
            },translation)
        return a_translation.strip()
       


