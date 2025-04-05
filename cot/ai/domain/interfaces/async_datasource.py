from typing import Dict


class IAsyncDatasource[Conn]:
    _connect: Conn
    def __init__(self,config: Dict = {}) -> None:
        self.config = config
        self._connect = None
    async def connect(self, **kwargs) -> Conn:
        pass
        
    async def disconnect(self, **kwargs) -> None:
        pass

    async def factory(self, **kwargs) -> Conn:
        pass
    
    async def init(self, **kwargs) -> None:
        pass
    
    async def destroy (self, **kwargs) -> None:
        pass