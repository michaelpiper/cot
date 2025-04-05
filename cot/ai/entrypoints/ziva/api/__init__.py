import asyncio

async def start_api(host: str = "127.0.0.1", port: int = 8000):
    from ..dependencies import container, engine
    from .app import app
    from ...utils.start_api import start_api as start
    container.wire(modules=[__name__])
    await engine.init()
    await start(app, host=host, port=port)
     
if __name__ == "__main__":
    asyncio.run(start_api())
    