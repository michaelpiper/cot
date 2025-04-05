from .....core.adapters.datasources import AsyncMongoDatasource
class AsyncZiVAMongoDatasource(AsyncMongoDatasource):
    async def init(self) -> None:
        conn = await self.factory()
        await self.disconnect(conn=conn)