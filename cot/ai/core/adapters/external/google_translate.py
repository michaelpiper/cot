# adapters/external/google_translate.py
from deep_translator import GoogleTranslator

from ....core.logger import logger
from ....domain.entities import TranslationRequest
from ....domain.interfaces import ITranslator
from httpx import AsyncClient
from ....domain.entities.transalation import TranslationRequest
from ....domain.interfaces import IAsyncTranslator

class GoogleTranslateAdapter(ITranslator):
    def translate(self, request: TranslationRequest) -> str:
        return GoogleTranslator(
            source=request.source_lang,
            target=request.target_lang
        ).translate(request.text)
        
        


class AsyncGoogleTranslateAdapter(IAsyncTranslator):
    def __init__(self, api_key: str):
        self.client = AsyncClient(base_url="https://translation.googleapis.com")
        self.api_key = api_key

    async def translate(self, request: TranslationRequest) -> str:
        res = await self.client.post(
            "/language/translate/v2",
            json={
                "q": request.text,
                "target": request.target_lang,
                "source": request.source_lang,
                "context": request.context
            },
            params={"key": self.api_key}
        )
        logger.info("translate json response %s %s",  {
                "q": request.text,
                "target": request.target_lang,
                "source": request.source_lang,
                "context": request.context
            },res.text,)
        body = res.json()
        return body["data"]["translations"][0]["translatedText"]


