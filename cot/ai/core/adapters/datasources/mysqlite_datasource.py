
from typing import Union
from ...logger import logger
from ....domain.interfaces import IDatasource
from sqlite3 import Connection, connect, Row

class MySQLiteDatasource(IDatasource[Connection]):
    
    @property
    def db_name(self):
        return self.config.get("DB_URL", None)
    @property
    def client(self) -> Union[Connection, None]:
        return self._connect
    
    def destroy(self, conn:Union[Connection, None], **kwargs) -> None:
        if not conn:
            self._connect = None
    def connect(self) -> Connection:
        if self._connect:
            return self._connect
        self._connect = self.factory()
        return self._connect
        
    def disconnect(self,conn:Union[Connection, None], **kwargs) -> None:
        if conn:
            conn.close()
        else:
            self._connect.close()
        self.destroy(**kwargs)

    def factory(self):
        database = self.config.get("DB_URL")
        db = connect(database)
        db.row_factory = Row
        logger.info(f"{database} connection open")
        return db 