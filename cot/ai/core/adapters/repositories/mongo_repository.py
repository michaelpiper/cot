
from ....domain.interfaces import IRepository
from ....domain.interfaces import IAsyncRepository
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as MotorClient
class MongoRepository(IRepository[MongoClient]):
    def connect (self, **kwargs)  -> MongoClient:
        return self.datasource.factory(**kwargs)
    def disconnect(self, conn:MongoClient, **kwargs):
        if isinstance(conn, MotorClient):
            conn.close()
            
class AsyncMongoRepository(IAsyncRepository[MotorClient]):
    async def connect (self, **kwargs)  -> MotorClient:
        return await self.datasource.factory(**kwargs)
    async def disconnect(self, conn:MotorClient, **kwargs):
        if isinstance(conn, MotorClient):
            conn.close()