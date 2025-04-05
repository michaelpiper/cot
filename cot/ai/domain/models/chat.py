from typing import Generator, List, Union
from .chat_bubble import ChatBubble

class Chat:
    def __init__(self, content:Union[str, Generator[str, str, str]], bubbles: Union[List[ChatBubble]]=None):
        self.content = content
        self.bubbles = bubbles if bubbles else []
        self.type = "text"  # Default type
        self.role = None  # Default role
        self.blockId = None
        self.id = None
        self.locale= 'en'
        self.locale_content = None
        self.lang = None
    def setBlockId(self, blockId):
        self.blockId = blockId
        return self
    def setLocale(self, locale):
        self.locale = locale
        return self
    
    def setLang(self, lang):
        self.lang = lang
        return self
    
    def setLocaleContent(self, locale_content):
        self.locale_content = locale_content
        return self
    
    def setId(self, id):
        self.id = id
        return self
   
    def setRole(self, role):
        self.role = role
        return self
    def setType(self, type):
        self.type = type
        return self
    
    def addBubble(self, bubble:ChatBubble):
        self.bubbles.append(bubble)
        return self

    def asText(self):
        self.type = "text"
        return self
    
    def asStream(self):
        self.type = "stream"
        return self
    
    def asImage(self):
        self.type = "image"
        return self

    def asAttachment(self):
        self.type = "attachment"
        return self  
    
    
    def isText(self):
        return self.type == "text"
    
    def isStream(self):
        return self.type == "stream"
    
    def isImage(self):
        return self.type == "image"

    def isAttachment(self):
        return  self.type == "attachment"  
    
    
    @classmethod
    def from_dict(cls, data: dict):
        chat = cls(content=data.get("content"), bubbles=[ChatBubble.from_dict(bubble) for bubble in  data.get("bubbles", [])],)
        if 'id' in data and data['id']:
            chat.setId(data["id"])
        if 'role' in data and data['role']:
            chat.setRole(data["role"])
        if 'role' in data and data['role']:
            chat.setType(data["role"])
        if 'blockId' in data and data['blockId']:
            chat.setBlockId(data["blockId"])
        if 'locale' in data and data['locale']:
            chat.setLocale(data["locale"])
        if 'locale_content' in data and data['locale_content']:
            chat.setLocaleContent(data["locale_content"])
        if 'lang' in data and data['lang']:
            chat.setLang(data["lang"])
        return chat
    
class UserChat(Chat):
    def __init__(self, content, bubbles=None):
        super(UserChat, self).__init__(content, bubbles)
        self.asUser()
 
    
    def asUser(self):
        self.role = "user"
        return self
class AssistantChat(Chat):
    def __init__(self, content, bubbles=None):
        super(AssistantChat, self).__init__(content, bubbles)
        self.asAssistant()
    def asAssistant(self):
        self.role = "assistant"
        return self