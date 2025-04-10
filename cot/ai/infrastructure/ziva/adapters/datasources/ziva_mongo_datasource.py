from .....core.adapters.datasources import AsyncMongoDatasource
class AsyncZiVAMongoDatasource(AsyncMongoDatasource):
    @property
    def connection_str(self):
        return self.config.get("MONGO_URI", None)
    async def init(self) -> None:
        conn = await self.factory()
        await self.disconnect(conn=conn)