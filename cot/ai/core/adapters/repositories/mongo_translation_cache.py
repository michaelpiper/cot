from typing import Optional
from ....domain.interfaces import ITranslationCache, IAsyncTranslationCache
from ....domain.entities import Translation
from .mongo_repository import MongoRepository, AsyncMongoRepository


class MongoTranslationCache(MongoRepository,ITranslationCache):
    def get(self, key: str) -> Optional[Translation]:
        client = self.connect()
        collection = client.translations.cache
        doc = collection.find_one({"key": key})
        result = Translation(**doc) if doc else None
        self.disconnect(conn=client)
        return result

    def set(self, key: str, translation: Translation) -> None:
        client = self.connect()
        collection = client.translations.cache
        collection.update_one(
            {"key": key},
            {"$set": translation.__dict__},
            upsert=True
        )
        
class AsyncMongoTranslationCache(AsyncMongoRepository,IAsyncTranslationCache):
    async def get(self, key: str) -> Optional[Translation]:
        client = await self.connect()
        collection = client.translations.cache
        doc = collection.find_one({"key": key})
        result = Translation(**doc) if doc else None
        await self.disconnect(conn=client)
        return result

    async def set(self, key: str, translation: Translation) -> None:
        client = await self.connect()
        collection = client.translations.cache
        collection.update_one(
            {"key": key},
            {"$set": translation.__dict__},
            upsert=True
        )
        await self.disconnect(conn=client)