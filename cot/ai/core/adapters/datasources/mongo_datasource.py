from typing import Union
from pymongo import MongoClient
from ....domain.interfaces import IDatasource
from ....core.logger import logger

class MongoDatasource(IDatasource[MongoClient]):
    @property
    def connection_str(self):
        return self.config.get("MONGO_URI", None)
    @property
    def client(self) -> Union[MongoClient, None]:
        return self._connect
    
    def destroy(self, **kwargs) -> None:
        if 'conn' not in kwargs:
            self._connect = None
        
    def connect(self) -> MongoClient:
        if self._connect:
            return self._connect
        self._connect = self.factory()
        return self._connect
        
    def disconnect(self, **kwargs) -> None:
        if 'conn' in kwargs:
            conn:MongoClient = kwargs['conn']
            conn.close()
        else:
            self._connect.close()
        self.destroy(**kwargs)
            

    def factory(self):
        connection_str = self.connection_str
        db =  MongoClient(connection_str)
        logger.info(f"{connection_str} connection open")
        return db 
    