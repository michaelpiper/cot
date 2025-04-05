from typing import Any, List, Union
from .datasource import IDatasource

class IFindOneRepository[Entity]:
    def find_one(self, **kwargs) -> Union[Entity, None]:
        pass
    
class IFindManyRepository[Entity]:
    def find_many(self, **kwargs) -> List[Entity]:
        pass
    
class ICreateRepository[Entity]:
    def create(self, model:Entity) -> List[Any]:
        pass
    
class IFindOneByIdRepository[Entity]:
    def find_one_by_id(self, id) -> Union[Entity, None]:
        pass
class IFindOneByRefRepository[Entity]:
    def find_one_by_ref(self, ref) -> Union[Entity, None]:
        pass
class IFindOneByNameRepository[Entity]:
    def find_one_by_name(self, name) -> Union[Entity, None]:
        pass   
class IUpdateByIdRepository:
    def update_by_id(self, id,  model) -> List[Any]:
        pass
 
class IUpdateRepository:
    def update(self, **kwargs) -> Any:
        pass 
class IUpdateManyRepository:
    def update_many(self, **kwargs) -> List[Any]:
        pass      
class IDeleteRepository:
    def delete(self, **kwargs) -> Any:
        pass  
class IDeleteManyRepository:
    def delete_many(self, **kwargs) -> List[Any]:
        pass      
class IDeleteByIdRepository:
    def delete_by_id(self, id) -> Any:
        pass
    
class IRepository[Conn]:
    def __init__(self, datasource: IDatasource[Conn]):
        self.datasource = datasource
    def connect (self, **kwargs) -> Conn:
        pass
    
    def disconnect (self, **kwargs) -> None:
        pass
    