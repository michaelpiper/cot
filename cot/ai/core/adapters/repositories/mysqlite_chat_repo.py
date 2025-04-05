import json

from ....core.logger import logger
from ....domain.models import Chat
from ....core.adapters.repositories import  MySQLiteRepository, AsyncMySQLiteRepository
from ....domain.interfaces import IAsyncChatRepository, IChatRepository

class MySQLiteChatRepository( MySQLiteRepository, IChatRepository):
    async def find_many(self, **kwargs):
        conn =  self.connect()
        cursor =  conn.cursor()
        
        query = "SELECT * from conversations where "
        for key in kwargs:
            query += "{}=?".format(key)
        query += ";"
        cursor.execute(query, [key for key in kwargs])
        results = cursor.fetchall()
        self.disconnect(conn=conn)
        return [Chat.from_dict(result) for result in results]     
          
    async def find_many_by_conversation_id(self, conversationId: str):
        results = self.find_many(blockId=conversationId)
        return results   
       
    async def create(self, chat: Chat):
        conn = self.connect()
        if chat.isStream():
            content = "".join(content for content in chat.content)
        else: 
            content = chat.content
        conn.execute("INSERT INTO conversations (role, type, content, blockId, metadata) VALUES(?, ?, ?, ?, ?);", [chat.role, chat.type, content, chat.blockId, json.dumps({"bubbles": [{"label": b.label, "value": b.value, "type": b.type} for b in chat.bubbles]})])
        conn.commit()
        self.disconnect(conn=conn)    
        
        
        
class AsyncMySQLiteChatRepository(AsyncMySQLiteRepository, IAsyncChatRepository):
    async def find_many(self, **kwargs):
        conn = await self.connect()
        cursor = await conn.cursor()
        
        query = "SELECT * from conversations where "
        for key in kwargs:
            query += "{}=?".format(key)
        query += ";"
        logger.info("query: %s value: %s", query, [f"{key}=>{kwargs[key]}" for key in kwargs])
        await cursor.execute(query, [kwargs[key] for key in kwargs])
        results = await cursor.fetchall()
        await cursor.close()
        await self.disconnect(conn=conn)
        def sanitize(metadata="{}",**kwargs):
            if isinstance(metadata, dict):
                pass
            elif isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata)
                except:
                    metadata = {}
            return {"bubbles":metadata.get("bubbles", []), **kwargs}
        return [Chat.from_dict(dict(sanitize(**result))) for result in results]     
          
    async def find_many_by_conversation_id(self, conversationId: str):
        results = await self.find_many(blockId=conversationId)
        return results   
       
    async def create(self, chat: Chat):
        conn = await self.connect()
        if chat.isStream():
            content = "".join(content for content in chat.content)
        else: 
            content = chat.content
        await conn.execute("INSERT INTO conversations (role, type, content, blockId, metadata) VALUES(?, ?, ?, ?, ?);", [chat.role, chat.type, content, chat.blockId, json.dumps({"bubbles": [{"label": b.label, "value": b.value, "type": b.type} for b in chat.bubbles], "locale": chat.locale, "locale_content": chat.locale_content, 'lang': chat.lang})])
        await conn.commit()
        await self.disconnect(conn=conn)    