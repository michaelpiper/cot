
# ChatBubble and Chat classes (mocked in Python)
class ChatBubble:
    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.type = "text"  # Default type
    def setType(self, type: str):
        self.type = type
        return self
    def asButton(self):
        self.type = "button"
        return self

    def asChip(self):
        self.type = "chip"
        return self

    def asLink(self):
        self.type = "link"
        return self

    def asText(self):
        self.type = "text"
        return self

    def asInput(self):
        self.type = "input"
        return self
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(data.get('label'), data.get("value")).setType(data.get('type', 'text'))
        
