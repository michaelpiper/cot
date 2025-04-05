import json
from typing import List, Union

from cot.ai.domain.interfaces.entity import IAsyncEntityRepository
from ....domain.models import Entity
from ....domain.interfaces import IEntityRepository
from .mysqlite_repository import AsyncMySQLiteRepository, MySQLiteRepository

class MySQLiteEntityRepository(MySQLiteRepository, IEntityRepository):
    def find_one_by_id (self, id) -> Entity | None:
        conn = self.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from conversation_entities where blockId=? and id=?;", (id,))
        result = cursor.fetchone()
        self.disconnect(conn=conn)
        
        if result:
            try:
                # Parse the JSON output
                value = json.loads(result['value'])
                return Entity.from_dict({**result, "value": value})
            except json.JSONDecodeError:
                # Fallback if the model doesn't return valid JSON
                return Entity.from_dict(result)
        return None    
    def update_or_create_by_conversation_id_and_key(self, conversationId: str, key: str, value: Union[str]) -> None:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id from conversation_entities where blockId=? and key=?;", (conversationId, key))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE conversation_entities SET value=? WHERE blockId = ? AND key=?;", (json.dumps(value), conversationId, key))   
        else:
            cursor.execute("INSERT INTO conversation_entities (blockId, key, value) VALUES (?,?,?);", (conversationId, key, json.dumps(value)))
        conn.commit()
        self.disconnect(conn=conn)
        
    def find_one_by_conversation_id_and_key(self, conversationId: str, key: Union[str, object]) -> Union[Entity, None]:
        conn = self.connect()
        cursor =conn.cursor()
        cursor.execute("SELECT * from conversation_entities where blockId=? and key=?;", (conversationId, key))
        result = cursor.fetchone()
        self.disconnect(conn=conn)
        
        if result:
            try:
                # Parse the JSON output
                value = json.loads(result['value'])
                return Entity.from_dict({**result, "value": value})
            except json.JSONDecodeError:
                # Fallback if the model doesn't return valid JSON
                return Entity.from_dict(result)
        return None
    
    def find_many_by_conversation_id(self, conversationId: str) -> List[Entity]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * from conversation_entities where blockId=?;", [conversationId])
        results =cursor.fetchall()
        self.disconnect(conn=conn)
        entities = []
        for result in results:
            try:
                # Parse the JSON output
                value = json.loads(result['value'])
                entities.append(Entity.from_dict({**result, "value": value}))
            except json.JSONDecodeError:
                entities.append(Entity.from_dict(result))
        return entities
    
    def get_one_by_conversation_id_and_key(self, conversationId: str, key: Union[str, object]) -> Union[Entity, None]:
       result = self.find_one_by_conversation_id_and_key(conversationId, key)
       if result: 
           return result.value
       return None
    def get_all_by_conversation_id(self, conversationId: str):
        results = self.find_many_by_conversation_id(conversationId)
        entities = {}
        for result in results:
            entities[result.key] = result.value  
        return entities
    
class AsyncMySQLiteEntityRepository(AsyncMySQLiteRepository, IAsyncEntityRepository):
    async def find_one_by_id (self, id) -> Entity | None:
        conn = await self.connect()
        cursor =await conn.cursor()
        await cursor.execute("SELECT * from conversation_entities where blockId=? and id=?;", (id,))
        result = cursor.fetchone()
        await self.disconnect(conn=conn)
        
        if result:
            try:
                # Parse the JSON output
                value = json.loads(result['value'])
                return Entity.from_dict({**result, "value": value})
            except json.JSONDecodeError:
                # Fallback if the model doesn't return valid JSON
                return Entity.from_dict(result)
        return None    
    async def update_or_create_by_conversation_id_and_key(self, conversationId: str, key: str, value: Union[str]) -> None:
        conn = await self.connect()
        cursor = await conn.cursor()
        await cursor.execute("SELECT id from conversation_entities where blockId=? and key=?;", (conversationId, key))
        result = await cursor.fetchone()
        if result:
            await cursor.execute("UPDATE conversation_entities SET value=? WHERE blockId = ? AND key=?;", (json.dumps(value), conversationId, key))   
        else:
            await cursor.execute("INSERT INTO conversation_entities (blockId, key, value) VALUES (?,?,?);", (conversationId, key, json.dumps(value)))
        await conn.commit()
        await self.disconnect(conn=conn)
        
    async def find_one_by_conversation_id_and_key(self, conversationId: str, key: Union[str, object]) -> Union[Entity, None]:
        conn = await self.connect()
        cursor =await conn.cursor()
        await cursor.execute("SELECT * from conversation_entities where blockId=? and key=?;", (conversationId, key))
        result = cursor.fetchone()
        await self.disconnect(conn=conn)
        
        if result:
            try:
                # Parse the JSON output
                value = json.loads(result['value'])
                return Entity.from_dict({**result, "value": value})
            except json.JSONDecodeError:
                # Fallback if the model doesn't return valid JSON
                return Entity.from_dict(result)
        return None
    
    async def find_many_by_conversation_id(self, conversationId: str) -> List[Entity]:
        conn = await self.connect()
        cursor = await conn.cursor()
        await cursor.execute("SELECT * from conversation_entities where blockId=?;", [conversationId])
        results =await cursor.fetchall()
        await cursor.close()
        await self.disconnect(conn=conn)
        entities = []
        for result in results:
            try:
                # Parse the JSON output
                value = json.loads(result['value'])
                entities.append(Entity.from_dict({**result, "value": value}))
            except json.JSONDecodeError:
                entities.append(Entity.from_dict(result))
        return entities
    
    async def get_one_by_conversation_id_and_key(self, conversationId: str, key: Union[str, object]) -> Union[Entity, None]:
       result = await self.find_one_by_conversation_id_and_key(conversationId, key)
       if result: 
           return result.value
       return None
    async def get_all_by_conversation_id(self, conversationId: str):
        results = await self.find_many_by_conversation_id(conversationId)
        entities = {}
        for result in results:
            entities[result.key] = result.value  
        return entities