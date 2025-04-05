import asyncio
from collections import abc
import functools
from typing import List

from ...domain.entities.transalation import TranslationRequest
from ...domain.models import ChatBubble
from ...domain.models import AsyncAIEngine
import json
from ...domain.models import Context
from ...core.contexts import EntityContext
from .contexts import ZiVAContext
from ...core.contexts import BubbleContext
from ...core.logger import logger
from ...domain.models import AssistantChat, UserChat
from ...domain.models import Conversation
from ...core.logger import logger
from collections.abc import Generator
from .config import ZiVAContainer

class ZiVAEngine(AsyncAIEngine):
    container:ZiVAContainer
    def __init__(self, container:ZiVAContainer):
        super(ZiVAEngine, self).__init__(container.genai_generator(), container.datasource())
        self.container = container
    async def init(self):
        await self.datasource.init()

    CAPABILITIES = [
        "1️⃣ Account Opening",
        "2️⃣ Account Reactivation",
        "3️⃣ Account Restriction",
        "4️⃣ Balance Enquiry",
        "5️⃣ Money Transfer",
        "6️⃣ Airtime Purchase",
        "7️⃣ Data Purchase",
        "8️⃣ Bills Payment",
        "9️⃣ Block Card",
        "🔟 Account Statement",
        "🔹 Log Complaints",
        "🔹 ATM/Branch Locator",
        "🔹 Agent Locator",
        "🔹 Reset PIN",
        "🔹 Loan Request",
    ]
    documents = [
        """
            ### **Instructions for Handling User Queries**
        - **Step-by-Step Guidance:**
        - Provide clear, structured instructions for banking processes.
        - Example:
        _"To transfer money, you can use the following methods:"_
        **1️⃣ Mobile App** – Go to Transfers > Enter Amount > Confirm
        **2️⃣ USSD** – Dial *123# and follow the prompts
        - **Security & Verification:**
        - If a user requests a **sensitive action** (e.g., resetting a PIN, blocking a card), ensure security verification steps are included.
        - Example:
            _"For security reasons, please confirm your registered phone number before proceeding with a PIN reset."_
        - **Handling Uncertainty & Edge Cases:**
        - If the user asks for a service the bank does **not** offer, politely inform them and suggest alternatives.
        - Example:
            _"I'm sorry, we currently do not support cryptocurrency transactions. However, you can check our available investment options."_
        """,
        """
        ### **Response Format Guidelines**
        ✅ Use polite, concise, and proactive language.
        ✅ Always structure responses in an easy-to-read format (bullets, numbered steps, etc.).
        ✅ If unsure about a user’s request, ask for **clarification** rather than making assumptions.
        ---
        ### **Example Interaction**
        - **User:** *hi*
            ✅ **ZiVA Response:**
            *"Hello! I'm ZiVA, your intelligent virtual banking assistant.
            How can I assist you with your banking needs today?
            You can check your balance, transfer money, pay bills, or block your card.
            Let me know what you’d like to do."*
        - **User:** *I want to block my ATM card. Someone stole it.*
            ✅ **ZiVA Response:**
            *"I understand the urgency. You can block your ATM card using any of the following methods:*
            🔹 **Mobile App** – Go to 'Card Services' > Select 'Block Card' > Confirm.
            🔹 **USSD** – Dial *123*4# and follow the prompts.
            🔹 **Customer Support** – Call our 24/7 helpline at +234-XXX-XXXX for immediate assistance."
        """,
    ]
    
    
    
        # Combined RAG + KG response
    def enhanced_retrieval(self, query):
        # Step 1: Vector search
        vector_results = self.retriever.retrieve(query)
        
        # Step 2: Extract entities (simplified)
        entities = ["money_transfer"]  # In reality, use NER model
        
        # Step 3: Knowledge graph expansion
        kg_context = self.kg.expand_query_context(query, entities)
        
        return {
            "documents": vector_results,
            "knowledge_graph": kg_context,
            "suggested_actions": self.generate_actions(kg_context)
        }

    def generate_actions(self, context: Context):
        actions = []
        for entity, data in context.items():
            if "regulations" in data:
                actions.append(f"Display compliance info for {entity}")
            if len(data["related_services"]) > 1:
                actions.append(f"Suggest bundle with {data['related_services'][0]['name']}")
        return actions

    # Example output for "international transfer rules":
    """
    {
        "documents": [
            {"text": "PSD2 requires SCA for transfers > €30", "score": 0.87},
            {"text": "SWIFT transfer fees apply", "score": 0.76}
        ],
        "knowledge_graph": {
            "money_transfer": {
                "regulations": [{"name": "PSD2"}],
                "related_services": []
            }
        },
        "suggested_actions": [
            "Display compliance info for money_transfer"
        ]
    }
    """

    async def generate_bubbles(self, user_input=[], entities: dict = {}, documents: List[str] = []):
        # Create bubble suggestions
        context = BubbleContext(generator=self.generator, **entities)
        await context.load_documents(documents)
        generated_text = await context.generate_text(user_input, self.CAPABILITIES)
        # Clean up the generated text to ensure valid JSON
        try:
            # Parse the JSON output
            bubbles = json.loads(generated_text)
        except json.JSONDecodeError:
            # Fallback if the model doesn't return valid JSON
            bubbles = []
        return bubbles

    # Function to extract entities from user input
    async def extract_entities(self, user_input):
        # System prompt for entity extraction
        context = EntityContext(generator=self.generator)
        try:
            # Use regex to extract the JSON part from the generated text
            generated_text = await context.generate_text(user_input)
            # Parse the JSON output
            entities = json.loads(generated_text)
        except json.JSONDecodeError:
            # Fallback if the model doesn't return valid JSON
            entities = {}
        return entities

    # Function to generate text
    async def generate_text(self, user_input=[], entities: dict = {}, documents: List[str] = []):
        # System prompt
        # Initialize context
        context = ZiVAContext(generator=self.generator, **entities)
        await context.load_documents(documents)
        #
        # print(json.dumps(prompt, indent=4, sort_keys=True,))
        # Generate a response using the model
        generated_text = await context.generate_text(user_input, self.CAPABILITIES)
        # print(f"prompt {prompt}")
        # print(generated_text)
        return generated_text
    async def retrieve_documents(self, query: str):
        return await asyncio.to_thread(
            lambda text: [embedding.text  for embedding in self.container.rag().retrieve(text) if embedding.score>7],
            query
        )
    # Function to handle conversation
    async def handle_conversation(self, conversation: Conversation):
        user_chat = conversation.get_last_chat()
        if user_chat.lang != user_chat.locale:
            translation_r = TranslationRequest(user_chat.content, source_lang= user_chat.lang, target_lang=user_chat.locale, context={})
            user_chat.locale_content =  await self.container.translate_uc().execute(translation_r)
        intent = None
        # prediction =  
        prediction, new_entities = await asyncio.gather(
            asyncio.to_thread(
                lambda text: self.container.intent_detector().predict(text),
                user_chat.content
            ),
            self.extract_entities(user_chat.content),
        )
    
        logger.info(
            "handle_conversation prompt: %s prediction: %s entities: %s",
            user_chat.content,
            prediction,
            new_entities,
        )
        intent = prediction[0]
        wait = []
        wait.append(self.container.chat_repo().create(user_chat))
        # print(json.dumps(conversation.get_chats_for_prompt(), indent=4, sort_keys=True,))

        logger.info("User Input: {}".format(user_chat.content))
        if new_entities:
            logger.info("New Entities detected: {}".format(new_entities))
            for entity_key in new_entities:
                # print("entity {}".format(entity_key))
                if new_entities[entity_key] != "N/A":
                    conversation.set_entity(entity_key, new_entities[entity_key])
                wait.append(
                    self.container.entity_repo().update_or_create_by_conversation_id_and_key(
                        conversation.id, entity_key, new_entities[entity_key]
                    )
                )
        if intent:
            logger.info("Intent: {}, {}".format(intent, user_chat.content))
        chats_for_prompt, docs = await asyncio.gather(
             asyncio.to_thread(
                functools.partial(conversation.get_chats_for_prompt),
                last=10
             ),
            
            self.retrieve_documents(
                user_chat.content
            )
        )
        logger.info("chats_for_prompt  length %d",  len(chats_for_prompt))
        logger.info("hybrid rag query docs length %d",  len(docs))
        generated_text, bubbles = await asyncio.gather(
            self.generate_text(
                chats_for_prompt,
                conversation.entities,
                docs
            ),
                
            self.generate_bubbles(
                chats_for_prompt,
                conversation.entities,
                documents= [""" - **Nigeria Pidgin** → `pcm` *(ISO 639-3, no ISO 639-1 exists)*  
        - **Yoruba** → `yo`  
        - **English** → `en`  
        - **French** → `fr`  
        - **Arabic** → `ar`  
        - **Hindi (India)** → `hi`
        
        **NOTE**: the output should be in \n"""+
                            f"**target language**: `{user_chat.lang}`"]
            ),
        )
        # Create a Chat object
        bubbles = [ChatBubble(b["label"], b["value"]).setType(b["type"]) for b in bubbles]
        
        if user_chat.lang != user_chat.locale:
            locale_content = ''
            if isinstance(generated_text, abc.Generator):
                for chunk in generated_text:
                    locale_content += chunk
            else: 
                locale_content = generated_text
            generated_lang = await self.container.detect_uc().execute(locale_content)
            if generated_lang == user_chat.lang:
                ai_chat = AssistantChat(locale_content, bubbles).setBlockId(conversation.id).asText().setLang(user_chat.lang).setLocale(user_chat.locale)
            else:
                translation_r = TranslationRequest(locale_content, source_lang=user_chat.locale, target_lang=user_chat.lang, context={})
                translated_content = await self.container.translate_uc().execute(translation_r) 
                ai_chat = AssistantChat(translated_content, bubbles).setBlockId(conversation.id).asText().setLang(user_chat.lang).setLocale(user_chat.locale).setLocaleContent(locale_content)
        else:
            ai_chat = AssistantChat(generated_text, bubbles).setBlockId(conversation.id).setLang(user_chat.lang).setLocale(user_chat.locale)
            if isinstance(generated_text, Generator):
                ai_chat.asStream()
            else:
                ai_chat.asText()

        wait.append(self.container.chat_repo().create(ai_chat))
        conversation.add_chat(ai_chat)
        await asyncio.gather(*wait)
        return ai_chat

    async def send_message(self, message: str, conversation: Conversation):
        # Send a POST request to the /chat endpoint
        locale = self.container.config.locale()
        lang = await self.container.detect_uc().execute(message)
        chat = UserChat(message).asText().setBlockId(conversation.id).setLocale(locale).setLang(lang)
        conversation.add_chat(chat)
        reply = await self.handle_conversation(conversation)
        if reply:
            return reply
        else:
            # print(f"Error: ")
            return None

    async def start_conversation(self, id) -> Conversation:
        conversation: Conversation = await super(ZiVAEngine, self).start_conversation(id)
         
        chats, entities = await asyncio.gather(
            self.container.chat_repo().find_many_by_conversation_id(conversation.id),
            self.container.entity_repo().get_all_by_conversation_id(conversation.id),
        )
        logger.info("start_conversation id: %s chats len %s entities %s",conversation.id, len(chats), entities)
        conversation.load_chats(chats)
        conversation.load_entities(entities)
        return conversation
