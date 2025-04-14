import asyncio
from collections import abc
import functools
from typing import List

from ...core.nlp.function_calling_context import FunctionCalllingPromptBuilder

from ...domain.entities.transalation import TranslationRequest
from ...domain.models import ChatBubble
from ...domain.models import AsyncAIEngine
import json
from ...domain.models import PromptBuilder
from ...core.nlp import EntityPromptBuilder
from .nlp.ziva_prompt_builder import ZiVAPromptBuilder
from ...core.nlp import BubblePromptBuilder
from ...core.logger import logger
from ...domain.models import AssistantChat, UserChat
from ...domain.models import Conversation
from ...core.logger import logger
from collections.abc import Generator
from .config import ZiVAContainer


class ZiVAEngine(AsyncAIEngine):
    container: ZiVAContainer

    def __init__(self, container: ZiVAContainer):
        super(ZiVAEngine, self).__init__(
            container.genai_generator(), container.datasource()
        )
        self.container = container

    async def init(self):
        await self.datasource.init()

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
            "suggested_actions": self.generate_actions(kg_context),
        }

    def generate_actions(self, context: PromptBuilder):
        actions = []
        for entity, data in context.items():
            if "regulations" in data:
                actions.append(f"Display compliance info for {entity}")
            if len(data["related_services"]) > 1:
                actions.append(
                    f"Suggest bundle with {data['related_services'][0]['name']}"
                )
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

    async def generate_bubbles(
        self, user_input=[], entities: dict = {}, documents: List[str] = []
    ):
        # Create bubble suggestions
        context = BubblePromptBuilder(generator=self.generator, **entities)
        await context.load_documents(documents)
        generated_text = await context.generate_text(
            user_input, self.container.config.capabilities()
        )
        # Clean up the generated text to ensure valid JSON
        try:
            # Parse the JSON output
            bubbles = json.loads(
                generated_text,
                parse_float=lambda input: float(input),
                parse_int=lambda input: int(input),
            )
        except json.JSONDecodeError:
            # Fallback if the model doesn't return valid JSON
            bubbles = []
        return bubbles

    async def generate_function_calling(
        self,
        user_input=[],
        entities: dict = {},
        documents: List[str] = [],
    ):
        # Create bubble suggestions
        context = FunctionCalllingPromptBuilder(generator=self.generator, **entities)
        await context.load_documents(documents)
        generated_text = await context.generate_text(
            user_input, [fun for fun in self.container.function_calls()]
        )
        # Clean up the generated text to ensure valid JSON
        try:
            # Parse the JSON output
            function_callings = json.loads(
                generated_text,
                parse_float=lambda input: float(input),
                parse_int=lambda input: int(input),
            )
        except json.JSONDecodeError:
            # Fallback if the model doesn't return valid JSON
            function_callings = None
        return function_callings

    # Function to extract entities from user input
    async def extract_entities(self, user_input):
        # System prompt for entity extraction
        context = EntityPromptBuilder(generator=self.generator)
        try:
            # Use regex to extract the JSON part from the generated text
            generated_text = await context.generate_text(user_input)
            # Parse the JSON output
            entities = json.loads(
                generated_text,
                parse_float=lambda input: float(input),
                parse_int=lambda input: int(input),
            )
        except json.JSONDecodeError:
            # Fallback if the model doesn't return valid JSON
            entities = {}
        return entities

    # Function to generate text
    async def generate_text(
        self, user_input=[], entities: dict = {}, documents: List[str] = []
    ):
        # System prompt
        # Initialize context
        context = ZiVAPromptBuilder(
            generator=self.generator,
            function_tools=[],
            **entities,
        )
        await context.load_documents(documents)
        #
        # print(json.dumps(prompt, indent=4, sort_keys=True,))
        # Generate a response using the model
        generated_text = await context.generate_text(
            user_input, self.container.config.capabilities()
        )

        try:
            # Use regex to extract the JSON part from the generated text
            # Parse the JSON output
            output = json.loads(
                generated_text,
                parse_float=lambda input: float(input),
                parse_int=lambda input: int(input),
            )
        except json.JSONDecodeError:
            # Fallback if the model doesn't return valid JSON
            output = {"text": generated_text, "bubbles": []}
        return output

    async def retrieve_documents(self, query: str):
        return await asyncio.to_thread(
            lambda text: [
                embedding.text
                for embedding in self.container.rag().retrieve(text)
                if embedding.score > 7
            ],
            query,
        )

    async def _translate_conversation(
        self,
        text: str,
        bubbles: List[ChatBubble],
        user_chat: UserChat,
        preferred_lang: str,
        conversation_id: str,
    ):
        if user_chat.lang != user_chat.locale:
            locale_content = ""
            if isinstance(text, abc.Generator):
                for chunk in text:
                    locale_content += chunk
            else:
                locale_content = text
            generated_lang = await self.container.detect_uc().execute(locale_content)
            if generated_lang == preferred_lang:
                ai_chat = (
                    AssistantChat(locale_content, bubbles)
                    .setBlockId(conversation_id)
                    .asText()
                    .setLang(preferred_lang)
                    .setLocale(user_chat.locale)
                )
            elif generated_lang == user_chat.lang:
                ai_chat = (
                    AssistantChat(locale_content, bubbles)
                    .setBlockId(conversation_id)
                    .asText()
                    .setLang(user_chat.lang)
                    .setLocale(user_chat.locale)
                    .setLocaleContent(locale_content)
                )
            else:
                translation_r = TranslationRequest(
                    locale_content,
                    source_lang=user_chat.locale,
                    target_lang=user_chat.lang,
                    context={},
                )
                translated_content = await self.container.translate_uc().execute(
                    translation_r
                )
                ai_chat = (
                    AssistantChat(translated_content, bubbles)
                    .setBlockId(conversation_id)
                    .asText()
                    .setLang(user_chat.lang)
                    .setLocale(user_chat.locale)
                    .setLocaleContent(locale_content)
                )
        else:
            ai_chat = (
                AssistantChat(text, bubbles)
                .setBlockId(conversation_id)
                .setLang(user_chat.lang)
                .setLocale(user_chat.locale)
                .setLocaleContent(text)
            )
            if isinstance(text, Generator):
                ai_chat.asStream()
            else:
                ai_chat.asText()

        return ai_chat

    # Function to handle conversation
    async def handle_conversation(self, conversation: Conversation):
        user_chat = conversation.get_last_chat()
        session = await self.container.session_manager().get(conversation.id)
        wait = []
        if user_chat.lang != user_chat.locale and user_chat.locale_content is None:
            translation_r = TranslationRequest(
                user_chat.content,
                source_lang=user_chat.lang,
                target_lang=user_chat.locale,
                fallback_lang= self.container.config.locale(),
                context={},
            )
            user_chat.locale_content = await self.container.translate_uc().execute(
                translation_r
            )

        chats_for_prompt, docs = await asyncio.gather(
            asyncio.to_thread(
                functools.partial(conversation.get_chats_for_prompt), last=10
            ),
            self.retrieve_documents(user_chat.content),
        )
        new_entities = await self.extract_entities(user_chat.content)
        preferred_lang = (
            conversation.entities.get("preferred_lang")
            if conversation.entities.get("preferred_lang") != "N/A"
            else user_chat.lang
        )

        logger.info(
            "handle_conversation prompt: %s entities: %s",
            user_chat.content,
            new_entities,
        )
        # return AssistantChat(user_chat.content).asText()

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
                        conversation.id,
                        entity_key,
                        new_entities[entity_key],
                    )
                )
        while True:
            logger.info("chats_for_prompt length %d", len(chats_for_prompt))
            logger.info("hybrid rag query docs length %d", len(docs))
            function_calling = await self.generate_function_calling(
                chats_for_prompt,
                conversation.entities,
                [
                    *docs,
                    self.container.generate_target_lang_doc_uc().execute(
                        preferred_lang,
                        self.container.supported_languges(),
                    ),
                ],
            )
            if function_calling:
                logger.info("Function Calling detected: {}".format(function_calling))

                result = await self.container.function_dispatcher().dispatch_function(
                    session_id=conversation.id,
                    name=function_calling["name"],
                    arguments=function_calling["arguments"],
                )
                logger.info(
                    "Function Calling {}: context=>{} next_step=>{}".format(
                        function_calling["name"], result.context, result.next_step
                    )
                )

                if result and result.next_step:
                    conversation.add_chat(
                        AssistantChat(result.next_step, result.bubbles).asText()
                    )
                    chats_for_prompt = await asyncio.to_thread(
                        functools.partial(conversation.get_chats_for_prompt),
                        last=10,
                    )
                    continue
                output = await self.generate_text(
                    chats_for_prompt,
                    conversation.entities,
                    [
                        *docs,
                        self.container.generate_target_lang_doc_uc().execute(
                            preferred_lang,
                            self.container.supported_languges(),
                        ),
                        f"\n\nUser PromptBuilder:\n{result.context}",
                    ],
                )

                if result:
                    logger.info("Function Calling result: {}".format(result))
                    preferred_lang = conversation.entities.get("preferred_lang")
                    ai_chat = await self._translate_conversation(
                        output["text"],
                        (
                            [
                                ChatBubble(b["label"], b["value"]).setType(b["type"])
                                for b in result.bubbles
                            ]
                            if result.bubbles
                            else [
                                ChatBubble(b["label"], b["value"]).setType(b["type"])
                                for b in output["bubbles"]
                            ]
                        ),
                        user_chat,
                        preferred_lang,
                        conversation_id=conversation.id,
                    )
                    wait.append(self.container.chat_repo().create(ai_chat))
                    conversation.add_chat(ai_chat)
                    await asyncio.gather(*wait)
                    return ai_chat

            output = await self.generate_text(
                chats_for_prompt,
                conversation.entities,
                [
                    *docs,
                    self.container.generate_target_lang_doc_uc().execute(
                        preferred_lang,
                        self.container.supported_languges(),
                    ),
                ],
            )

            # Create a Chat object
            bubbles = [
                ChatBubble(b["label"], b["value"]).setType(b["type"])
                for b in output["bubbles"]
            ]
            ai_chat = await self._translate_conversation(
                output["text"],
                bubbles,
                user_chat,
                preferred_lang,
                conversation_id=conversation.id,
            )
            wait.append(self.container.chat_repo().create(ai_chat))
            conversation.add_chat(ai_chat)
            await asyncio.gather(*wait)
            return ai_chat

    async def send_message(self, message: str, conversation: Conversation):
        # Send a POST request to the /chat endpoint
        locale: str = self.container.config.locale()
        lang = await self.container.detect_uc().execute(message)
        chat = (
            UserChat(message)
            .asText()
            .setBlockId(conversation.id)
            .setLocale(locale)
            .setLang(lang)
        )
        if locale == lang:
            chat.setLocaleContent(message)
        conversation.add_chat(chat)
        reply = await self.handle_conversation(conversation)
        if reply:
            return reply
        else:
            return None

    async def start_conversation(self, id) -> Conversation:
        conversation: Conversation = await super(ZiVAEngine, self).start_conversation(
            id
        )

        chats, entities = await asyncio.gather(
            self.container.chat_repo().find_many_by_conversation_id(conversation.id),
            self.container.entity_repo().get_all_by_conversation_id(conversation.id),
        )
        logger.info(
            "start_conversation id: %s chats len %s entities %s",
            conversation.id,
            len(chats),
            entities,
        )
        conversation.load_chats(chats)
        conversation.load_entities(entities)
        return conversation
