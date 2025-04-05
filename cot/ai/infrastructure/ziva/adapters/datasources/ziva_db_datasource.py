
import asyncio
from .....core.adapters.datasources import AsyncMySQLiteDatasource

class AsyncZiVADatasource(AsyncMySQLiteDatasource):
    async def init(self) -> None:
        conn = await self.factory()
        await asyncio.gather(
        conn.execute(""" 
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            grades TEXT NOT NULL
        );
        """),
        conn.execute(""" 
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL,
            role TEXT NOT NULL,
            blockId TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT NULL default NULL
        );
        """) , 
        conn.execute(""" 
        CREATE TABLE IF NOT EXISTS conversation_entities (
            id INTEGER PRIMARY KEY,
            blockId TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NULL default NULL
        );
        """) 
        ) 
        await conn.commit()
        await self.disconnect(conn=conn)