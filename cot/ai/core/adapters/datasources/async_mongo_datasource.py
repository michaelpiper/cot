from typing import Union
from motor.motor_asyncio import AsyncIOMotorClient as MotorClient
from ....domain.interfaces.async_datasource import IAsyncDatasource
from ....core.logger import logger

class AsyncMongoDatasource(IAsyncDatasource[MotorClient]):
    @property
    def connection_str(self):
        return self.config.get("MONGO_URI", None)
    @property
    def client(self) -> Union[MotorClient, None]:
        return self._connect
    
    async def destroy(self, conn:Union[MotorClient, None], **kwargs) -> None:
        if not conn:
            self._connect = None
        
    async def connect(self) -> MotorClient:
        if self._connect:
            return self._connect
        self._connect = await self.factory()
        return self._connect
        
    async def disconnect(self,  conn:Union[MotorClient, None],**kwargs) -> None:
        if conn:
            await conn.close()
        else:
            await self._connect.close()
        await self.destroy(conn=conn, **kwargs)
            

    async def factory(self):
        connection_str = self.connection_str
        db =  MotorClient(connection_str)
        logger.info(f"{connection_str} connection open")
        return db 
    