
from collections import abc
from typing import Any, Callable, Optional, Dict, List
from ....domain.models import PromptBuilder
import json
from ... import logger
class GeneralPromptBuilder(PromptBuilder):
    def __init__(
        self,
        generator: Callable[[List[Any], Dict], str],
        name: str = None,
        location: str = None,
        email: str = None,
        phone: str = None,
        preferences: Optional[Dict] = None,
        tasks: Optional[List[str]] = None,
        **kwargs,
    ):
        """
        Initialize the PromptBuilder class with user-specific information.
        """
        super(GeneralPromptBuilder, self).__init__(generator, **kwargs)
        self.name = name if name else "N/A"
        self.location = location if location else "N/A"
        self.email = email if email else "N/A"
        self.phone = phone if phone else "N/A"
        self.preferences = preferences if preferences else {
            "email_signature": f"Best regards,\n{self.name}",
            "whatsapp_signature": "Sent via Piper AI",
            "sms_signature": "Sent via Piper AI",
        }
        self.tasks = tasks if tasks else []

    @property
    def name(self) -> str:
        return self["name"]

    @name.setter
    def name(self, value: str):
        self["name"] = value

    @property
    def location(self) -> str:
        return self["location"]

    @location.setter
    def location(self, value: str):
        self["location"] = value

    @property
    def email(self) -> str:
        return self["email"]

    @email.setter
    def email(self, value: str):
        self["email"] = value

    @property
    def phone(self) -> str:
        return self["phone"]

    @phone.setter
    def phone(self, value: str):
        self["phone"] = value

    @property
    def preferences(self) -> Dict:
        return self["preferences"]

    @preferences.setter
    def preferences(self, value: Dict):
        self["preferences"] = value

    @property
    def tasks(self) -> List[str]:
        return self["tasks"]

    @tasks.setter
    def tasks(self, value: List[str]):
        self["tasks"] = value

    def add_task(self, task: str) -> str:
        """
        Add a task to the context.
        """
        self.tasks.append(task)
        return f"Task added: {task}"

    def update_preference(self, key: str, value: str) -> str:
        """
        Update a preference in the context.
        """
        if key in self.preferences:
            self.preferences[key] = value
            return f"Preference updated: {key} = {value}"
        else:
            return f"Preference '{key}' not found."

    def get_system_prompt(self) -> str:
        """
        Generate a system prompt based on the current context.
        """
        system_prompt = f"""
        You are Piper AI, a highly intelligent and personalized assistant for user. 
        Your goal is to assist user in completing tasks efficiently and effectively.
        
        Here is the current context about the user:
{"\n".join(f"        - {key}: {json.dumps(self[key])}" for key in self)}
       
        You have access to the following functionalities:
        1. Send emails.
        2. Send WhatsApp messages.
        3. Send SMS.
        4. Remember tasks and reminders.
        5. Check Balance
        
        Always be polite, concise, and proactive. If you don't understand something, ask for clarification.
        """
        
        if self.tasks:
            system_prompt += "\n\n        Remembered tasks:\n"
            for task in self.tasks:
                system_prompt += f"        - {task}\n"
        
        return system_prompt
    def generate_text(self, user_input=[]):
        # Function to generate text
        # System prompt
        system_prompt = self.get_system_prompt()
        logger.info("System Input: {}".format(system_prompt))
        # Initialize context
        prompt  =   [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text":system_prompt}, 
                    ]
                },
            ] + user_input 
        # 
        # print(json.dumps(prompt, indent=4, sort_keys=True,))
        # Generate a response using the model
        response = self.generator(
            prompt, 
            max_new_tokens=500,
            # truncation=True,
            num_return_sequences=1, 
        )
        
        if isinstance(response, abc.Generator):
            generated_text = ""
            for output in response:
                generated_text += output
        else:
            generated_text = response 
        logger.info("Generated Text: {}".format(generated_text))
        return generated_text