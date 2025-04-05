import os
from ...infrastructure.ziva.config import ZiVAContainer
from ...infrastructure.ziva.engine import ZiVAEngine

container = ZiVAContainer()
    # Initialize DI container
container.wire(modules=[__name__])
container.config.from_dict({
    "locale": 'en',
    "google_api_key": os.getenv("GOOGLE_API_KEY"),
    "mongo_uri": os.getenv("MONGO_URI"),
    "sqlite_database_name": os.getenv("MYSQLITE_DB_NAME"),
})
engine = ZiVAEngine(container)