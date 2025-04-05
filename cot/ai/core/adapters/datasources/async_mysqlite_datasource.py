
from typing import Optional
from ...logger import logger
from ....domain.interfaces import IAsyncDatasource
from aiosqlite import Connection, connect, Row

class AsyncMySQLiteDatasource(IAsyncDatasource[Connection]):
    
    @property
    def db_name(self):
        return self.config.get("DB_URL", None)
    @property
    def client(self) -> Optional[Connection]:
        return self._connect
    
    async def destroy(self, conn:Optional[Connection], **kwargs) -> None:
        if not conn:
            self._connect = None
        
    async def connect(self) -> Connection:
        if self._connect:
            return self._connect
        self._connect = await self.factory()
        return self._connect
        
    async def disconnect(self, conn: Optional[Connection], **kwargs) -> None:
        if conn:
            await conn.close()
        else:
            await self._connect.close()
        await self.destroy(conn=conn, **kwargs)

    async def factory(self):
        database = self.config.get("DB_URL")
        db = await connect(database)
        db.row_factory = Row
        logger.info(f"{database} connection open")
        return db 