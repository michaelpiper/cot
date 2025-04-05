class Entity:
    def __init__(self, id=None, key=None, value=None, blockId= None) -> None:
        self.id = id
        self.blockId = blockId
        self.key = key
        self.value = value
    @classmethod 
    def from_dict(cls, data: dict):
        return cls(id=data.get("id"), key=data.get('key'), value=data.get("value"), blockId= data.get("blockId"))
    
    def to_dict(self):
        return dict(id=self.id, key=self.key, value=self.value, blockId=self.blockId)
        
        