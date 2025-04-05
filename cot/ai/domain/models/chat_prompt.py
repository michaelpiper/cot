class ChatPrompt(list):
    def __init__(self, *args, **kwargs):
        """
        Initialize the ChatPrompt object as a list.
        """
        super(ChatPrompt, self).__init__(*args, **kwargs)
    
    def convert_to_chat_history(self, last=None):
        # 1. Start with the processed promp_chats and reconstruct the original history
        chat_history = []
        for prompt in self:
            if last and len(chat_history) == last:
                # If slicing occurred in original, we can't recover the full history
                # We can only return what we have
                return chat_history
            role = prompt['role']
            for content_item in prompt['content']:
                content_type = content_item['type']
                content_value = content_item[content_type]
                chat_history.append({
                    'role': role,
                    'type': content_type,
                    'content': content_value
                })

        # 2. Handle the slicing reversal
        # The original code had conditional slicing with 'last' parameter
        # To reverse, we need to know if slicing occurred
        return chat_history
    @classmethod
    def from_str(cls, input):
        return cls([
            {"role":"user", "content":[{"type": "text","text":input}]}
        ])
      
    def add_user_content(self, content, type= 'text'):
        self.add_content('user',content, type)   
    def add_assistant_content(self, content, type= 'text'):
        self.add_content('assistant',content, type)
    def add_content(self,role, content, type= 'text'):
        prompt = self[-1]
        if prompt and prompt.get("role") == role:
            prompt = prompt  
        else:
            prompt = None
        if not prompt:
            prompt = {
                "content": [],
                "role": role
            }
            self.append( prompt)
        if not isinstance (prompt.get('content'), list):
            prompt['content'] = []
        prompt['content'].append({
            "type": type,
            f"{type}": content
        })  
    def add_system_content(self, content, type= 'text'):
        system_prompt= None
        for prompt in self:
            if prompt.get("role") == "system":
                system_prompt = prompt
            
        if not system_prompt:
            system_prompt = {
                "content": [],
                "role": "system"
            }
            self.insert(0, system_prompt)
        if not isinstance (system_prompt.get('content'), list):
            system_prompt['content'] = []
        system_prompt['content'].append({
            "type": type,
            f"{type}": content
        })
             
        
    def get_system_content(self):
        """
        Get the content of the first system message in the chat prompts.
        Returns None if no system message is found.
        """
        for prompt in self:
            if prompt.get("role") == "system":
                # Extract the text from the content array
                content = prompt.get("content", [])
                system_content= ''
                for item in content:
                    if item.get("type") == "text":
                        system_content += item.get("text")
                return system_content
        return None  # Return None if no system message is found

    def get_last_user_content(self):
        """
        Get the content of the last user message in the chat prompts.
        Returns None if no user message is found.
        """
        for prompt in reversed(self):  # Iterate in reverse to find the last user message
            if prompt.get("role") == "user":
                # Extract the text from the content array
                content = prompt.get("content", [])
                for item in content:
                    if item.get("type") == "text":
                        return item.get("text")
        return None  # Return None if no user message is found
    def validate_structure(self):
        """
        Validate the structure of the chat prompts.
        Raises ValueError if the structure is invalid.
        """
        for prompt in self:
            if not isinstance(prompt, dict):
                raise ValueError("Each prompt must be a dictionary.")
            if "role" not in prompt or "content" not in prompt:
                raise ValueError("Each prompt must have 'role' and 'content' keys.")
            if not isinstance(prompt["content"], list):
                raise ValueError("The 'content' field must be a list.")
            for item in prompt["content"]:
                if not isinstance(item, dict):
                    raise ValueError("Each item in 'content' must be a dictionary.")
                if "type" not in item or "text" not in item:
                    raise ValueError("Each item in 'content' must have 'type' and 'text' keys.")