from datetime import datetime, timezone
import json
from typing import Any, Dict

from .....core.logger import logger
from .....core.adapters.repositories.mongo_repository import AsyncMongoRepository
from .....domain.models.session import Session
from .....domain.interfaces.encryptor import IEncryptor
from .....domain.interfaces.session_repository import ISessionRepository


class MongoSessionRepository(AsyncMongoRepository, ISessionRepository):
    def __init__(self, encryptor: IEncryptor, *args, **kwargs):
        super(MongoSessionRepository, self).__init__(*args, **kwargs)
        self.encrypt = encryptor

    async def get(self, session_id: str) -> Session:
        conn = await self.connect()
        db = conn.get_default_database()
        session_collection = db.session
        session = await session_collection.find_one(
            {"session_id": session_id}
        )
        logger.info("session: {}".format(session))
        await self.disconnect(conn=conn)
        if not session:
            return Session(session_id=session_id)
        if not session.get("encrypted") or not session.get("encrypted_data"):
            return Session.from_dict(session)
       
        return Session.from_dict(
            {
                "session_id": session.get("session_id"),
                "created_at": session.get("created_at"),
                "last_accessed": session.get("last_accessed"),
                "data": await self._decrypt(session["encrypted_data"]),
            }
        )

    async def _encrypt(self, data: Dict):
        data = json.dumps(data)
        return self.encrypt.encrypt(data)

    async def _decrypt(self, data: Any) -> Dict:
        
        decrypted_text = self.encrypt.decrypt(data)
        logger.info("decrypted_text: {}".format(decrypted_text))
        
        try:
            decrypted_data = json.loads(
                decrypted_text,
                parse_float=lambda input: float(input),
                parse_int=lambda input: int(input),
            )
            return decrypted_data
        except Exception as e:
            return {}

    async def save(self, session: Session) -> Session:
        conn = await self.connect()
        db = conn.get_default_database()
        session_collection = db.session

        await session_collection.update_one(
            {"session_id": session.session_id},
            {
                "$set": {
                    "session_id": session.session_id,
                    "last_accessed": session.last_accessed,
                    "encrypted": True,
                    "encrypted_data":await self._encrypt(session.data),
                    "updated_at": datetime.now(timezone.utc)
                },
                "$setOnInsert": {  # Only set on document creation
                    "created_at": session.created_at
                },
            },
            upsert=True,
        )
