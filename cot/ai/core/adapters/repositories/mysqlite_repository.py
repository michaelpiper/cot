from aiosqlite import Connection
from sqlite3 import Connection as MySQLiteConnection
from ....domain.interfaces import IRepository


class MySQLiteRepository(IRepository[MySQLiteConnection]):
    def connect (self, **kwargs)  -> MySQLiteConnection:
        return self.datasource.factory(**kwargs)
    def disconnect(self, conn:MySQLiteConnection, **kwargs):
        if isinstance(conn, MySQLiteConnection):
            conn.close()
            
class AsyncMySQLiteRepository(IRepository[Connection]):
    async def connect (self, **kwargs)  -> Connection:
        return await self.datasource.factory(**kwargs)
    async def disconnect(self, conn:Connection, **kwargs):
        if isinstance(conn, Connection):
            await conn.close()