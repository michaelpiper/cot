# adapters/external/langdetect_adapter.py
from ....domain.interfaces import ILanguageDetector
from ....domain.interfaces import IAsyncLanguageDetector

class LangDetectAdapter(ILanguageDetector):
    def detect(self, text: str) -> str:
        import langid
        try:
            return langid.classify(text)[0]
        except:
            return "en"



class AsyncLangDetectAdapter(IAsyncLanguageDetector):
    async def detect(self, text: str) -> str:
        # Wrap sync lib in async executor
        import asyncio
        import langid
        return await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: langid.classify(text)[0]
        )