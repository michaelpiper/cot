from typing import Any, List, Union
from .async_datasource import IAsyncDatasource

class IAsyncFindOneRepository[Entity]:
    async def find_one(self, **kwargs) -> Union[Entity, None]:
        pass
    
class IAsyncFindManyRepository[Entity]:
    async def find_many(self, **kwargs) -> List[Entity]:
        pass
    
class IAsyncCreateRepository[Entity]:
    async def create(self, model: Entity) -> List[Any]:
        pass
    
class IAsyncFindOneByIdRepository[Entity]:
    async def find_one_by_id(self, id) -> Union[Entity, None]:
        pass
class IAsyncFindOneByRefRepository[Entity]:
    async def find_one_by_ref(self, ref) -> Union[Entity, None]:
        pass
class IAsyncFindOneByNameRepository[Entity]:
    async def find_one_by_name(self, name) -> Union[Entity, None]:
        pass   
class IAsyncUpdateByIdRepository:
    async def update_by_id(self, id,  model) -> List[Any]:
        pass
 
class IAsyncUpdateRepository:
    async def update(self, **kwargs) -> Any:
        pass 
class IAsyncUpdateManyRepository:
    async def update_many(self, **kwargs) -> List[Any]:
        pass      
class IAsyncDeleteRepository:
    async def delete(self, **kwargs) -> Any:
        pass  
class IAsyncDeleteManyRepository:
    async def delete_many(self, **kwargs) -> List[Any]:
        pass      
class IAsyncDeleteByIdRepository:
    async def delete_by_id(self, id) -> Any:
        pass
    
class IAsyncRepository[Conn]:
    def __init__(self, datasource: IAsyncDatasource[Conn]):
        self.datasource = datasource
    async def connect (self, **kwargs) -> Conn:
        pass
    
    async def disconnect (self, **kwargs) -> None:
        pass
    