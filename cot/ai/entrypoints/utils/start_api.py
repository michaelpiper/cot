
from flask import Flask
# import uvicorn

async def start_api(
    app: Flask,
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = False
):
    """Run the API server"""
    # config = uvicorn.Config(
    #      app,
    #     host=host,
    #     port=port,
    #     reload=reload,
    #     log_level="info"
    # )
    # server = uvicorn.Server(config)
    # await server.serve()
    app.run( host=host,
        port=port,
        debug= not reload,
        )