

import json
from ...core.contexts import EntityContext
from .contexts import GeneralContext
from ...core.contexts import BubbleContext
from .....scripts.startup.engine import add_chat_to_db
from ...domain.models import AssistantChat
from ...domain.models import Conversation
from ...domain.models import Frame
from ...core.logger import logger

class GeneralFrame(Frame):
    def generate_bubbles(self, user_input= [], entities: dict = {} ):
        # Create bubble suggestions
        context = BubbleContext(
            generator=self.generator,
            **entities
        )
        generated_text = context.generate_text(user_input)
        # Clean up the generated text to ensure valid JSON
        try:
            # Parse the JSON output
            bubbles = json.loads(generated_text)
        except json.JSONDecodeError:
            # Fallback if the model doesn't return valid JSON
            bubbles = []
        return bubbles
    
    # Function to extract entities from user input
    def extract_entities(self, user_input):
        # System prompt for entity extraction
        context = EntityContext(
            generator=self.generator
        )
        try:
            # Use regex to extract the JSON part from the generated text
            generated_text = context.generate_text(user_input)
            # Parse the JSON output
            entities = json.loads(generated_text)
        except json.JSONDecodeError:
            # Fallback if the model doesn't return valid JSON
            entities = []
        return entities
    
    # Function to generate text
    def generate_text(self, user_input = [], entities: dict = {}):
        # System prompt
        # Initialize context
        context = GeneralContext(
            generator=self.generator,
            **entities
        )
        # 
        # print(json.dumps(prompt, indent=4, sort_keys=True,))
        # Generate a response using the model
        generated_text = context.generate_text(user_input)
        # print(f"prompt {prompt}")
        # print(generated_text)
        return generated_text




    # Function to handle conversation
    def handle_conversation(self, conversation: Conversation):
        user_chat = conversation.get_last_chat()
        intent = None
        # intent, _confidence = predict_intent(user_chat.content)
        new_entities = self.extract_entities(user_chat.content)
        add_chat_to_db(user_chat)
        # print(json.dumps(conversation.get_chats_for_prompt(), indent=4, sort_keys=True,))
    
        logger.info("User Input: {}".format(user_chat.content))
        if new_entities:
            logger.info("New Entities detected: {}".format(new_entities))
            for entity_key in new_entities:
                # print("entity {}".format(entity_key))
                if new_entities[entity_key] != "N/A":
                    conversation.set_entity(entity_key, new_entities[entity_key])
                    self.set_conversation_entity(conversation.id, entity_key, new_entities[entity_key])
        if intent:
            logger.info("Intent: {}, {}".format(intent, user_chat.content))
        if intent == "check_balance":
            # from ....intent.check_balance import check_balance
            # from ....contexts import CheckBalanceContext
            # new_entities = check_balance(**conversation.entities)
            # if new_entities:
            #     for entity_key in new_entities:
            #         # print("entity {}".format(entity_key))
            #         if new_entities[entity_key] != "N/A":
            #             conversation.set_entity(entity_key, new_entities[entity_key])
            bubbles = []
            context = self.generate_text(conversation.get_chats_for_prompt(last=5), conversation.entities)
            generated_text = context.generate_text(conversation.get_chats_for_prompt(last=5), conversation.entities)
            ai_chat = AssistantChat(generated_text, bubbles).asText().setBlockId(conversation.id) 
            add_chat_to_db(ai_chat)
            conversation.add_chat(ai_chat)
            return ai_chat
        if intent == "send_email":
            # from ....intent.send_email import send_email
            # send_email("Subject", "Body", "recipient@example.com")
            bubbles = []
            ai_chat = AssistantChat("Email sent!", bubbles).asText().setBlockId(conversation.id) 
            add_chat_to_db(ai_chat)
            conversation.add_chat(ai_chat)
            return ai_chat
        elif intent == "send_whatsapp":
            # from ....intent.send_whatsapp_message import send_whatsapp_message
            # send_whatsapp_message("+1234567890", "Hello from Piper AI!")
            bubbles= []
            ai_chat = AssistantChat("WhatsApp message sent!", bubbles).asText().setBlockId(conversation.id) 
            add_chat_to_db(ai_chat)
            conversation.add_chat(ai_chat)
            return ai_chat
        elif intent == "send_sms":
            # from ...end_sms import send_sms
            # send_sms("+1234567890", "Hello from Piper AI!")
            bubbles= []
            ai_chat =  AssistantChat("SMS sent!", bubbles).asText().setBlockId(conversation.id) 
            add_chat_to_db(ai_chat)
            conversation.add_chat(ai_chat)
            return ai_chat
        else:
            generated_text = self.generate_text(conversation.get_chats_for_prompt(last=5), conversation.entities)
            bubbles =[]
            # bubbles = [ChatBubble( b['label'], b['value']).setType(b['type']) for b in  generate_bubbles(conversation.get_chats_for_prompt(last=5), conversation.entities)]
            # Create a Chat object
            ai_chat = AssistantChat(generated_text, bubbles).asText().setBlockId(conversation.id)
            add_chat_to_db(ai_chat)
            conversation.add_chat(ai_chat)
            return ai_chat