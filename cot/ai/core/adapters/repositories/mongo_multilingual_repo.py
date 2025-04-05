from typing import Dict
from .mongo_repository import AsyncMongoRepository, MongoRepository
from ....domain.interfaces import  ILocalizationRepository
class MongoMultilingualRepository(MongoRepository, ILocalizationRepository[Dict[str, str]]):  
    def get_localized_terms(self, locale: str) -> Dict[str, str]:
        conn =  self.connect()
        collection = conn.banking.i18n
        doc = collection.find_one({"locale": locale})
        result = doc["terms"] if doc else {}
        self.disconnect(conn=conn)
        return result  
          
class AsyncMongoMultilingualRepository(AsyncMongoRepository, ILocalizationRepository[Dict[str, str]]):  
    async def get_localized_terms(self, locale: str) -> Dict[str, str]:
        conn = await self.connect()
        collection = conn.banking.i18n
        doc = await collection.find_one({"locale": locale})
        result = doc["terms"] if doc else {}
        await self.disconnect(conn=conn)
        return result