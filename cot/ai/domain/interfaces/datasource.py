from typing import Dict


class IDatasource[Conn]:
    _connect: Conn
    def __init__(self, config: Dict = {}) -> None:
        self.config = config
        self._connect = None
    def connect(self, **kwargs) -> Conn:
        pass
        
    def disconnect(self, **kwargs) -> None:
        pass

    def factory(self, **kwargs) -> Conn:
        pass
    
    def init(self, **kwargs) -> None:
        pass
    
    def destroy (self, **kwargs) -> None:
        pass