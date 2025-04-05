import json
from typing import List, Self, Union, Any
from .chat import Chat
from .chat_bubble import ChatBubble
from ... import logger

class Conversation:
    def __init__(self, id: str, history:List[Chat]=[], entities = {}) -> None:
        self.id = id
        self.history = history if history else []
        self.entities = entities if entities else {}
        # self.message = None
        
    # def get_user_input(self) -> str:
    #     return "{}".format(self.message)
    
    # def set_user_input(self, message: str):
    #     self.message = message
        
    def set_entity(self, entity_key: str, entity_value: Union[str, object]) -> Self:
        self.entities[entity_key] = entity_value
        return self
    def get_entity(self, entity_key: str) :
        return self.entities[entity_key] 
    def load_entities (self, entities: dict):
        self.entities.clear() 
        for entity_key in entities:
            self.entities[entity_key] = entities[entity_key]
        return self
    def load_chats(self, chats: List[Chat]) :
        self.history.clear()
        for chat in chats:
            self.history.append(chat)
        return self
    def load_chats_from_dict(self, chats: List[Any]) :
        self.history.clear()
        for chat in chats:
            logger.info("load_chats %s", type(chat))
            try:
                metadata = json.load(chat['metadata'])
            except:
                metadata = {}
            bubbles = metadata.get('bubbles', [])
            bubbles = [ ChatBubble(bubble['label'], bubble['value']).setType(bubble['type']) for bubble in  bubbles]
            self.history.append(
                Chat(chat['content'], bubbles)
                .setBlockId(chat["blockId"])
                .setId(chat["id"])
                .setRole(chat["role"])
                .setType(chat["type"])
            )
        return self
    def add_chat(self, chat: Chat) -> Self:
        self.history.append(chat)
        return self
    def add_chat(self, *args) -> Self:
        if len(args) == 1 and isinstance(args[0], Chat):
            # If a Chat object is passed, add it directly
            self.history.append(args[0])
        elif len(args) == 3:
            # If role, type, and content are passed, create a Chat object
            role, type, content = args
            self.history.append(Chat(content).setType(type).setRole(role))
        else:
            raise ValueError("Invalid arguments for add_chat")
        return self
    def get_chats(self):
        return self.history
    def get_chats_except_last(self):
        return self.history[:-1]
    def get_last_chat(self):
        if self.history:  # Check if the history is not empty
            return self.history[-1]
        else:
            return None
    def get_last_message(self):
        if self.history:  # Check if the history is not empty
            return self.history[-1].content
        else:
            return None
    def get_last_user_chat(self):
        for chat in reversed(self.history):
            if chat.role == "user":
                return chat
        return None
    def get_last_user_message(self):
        for chat in reversed(self.history):
            if chat.role == "user":
                return chat.content
        return None
    def get_chats_for_prompt(self, last=None):
         # Get the last 'last' chats from the history
        last_chats = self.history[-last:] if last and len(self.history) > last else self.history

        promp_chats = []
        current_role = None
        for chat in last_chats:
            if len(promp_chats) ==0 and chat.role != "user":
                pass
            elif chat.role != current_role:
               current_role =  chat.role
               promp_chats.append({
                   "role": current_role,
                   "content": []
               })
            if(len(promp_chats)>0):
                promp_chats[-1]['content'].append({"type": chat.type, f"{chat.type}":chat.content })
        return promp_chats
    