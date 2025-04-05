from ...domain.interfaces import IAsyncAIEngine,  IAIEngine

class CoTCLI:
    def run(self, engine: IAIEngine):
          # Start a new conversation
        conversation_id = input("Chat ID: ")
        conversation = engine.start_conversation(conversation_id)
        print(f"Started new conversation with ID: {conversation.id}")

        # print(json.dumps(conversation.get_chats_for_prompt(), indent=4, sort_keys=True,))
    
        while True:
            # Get user input
            message = input("You: ")
            # Exit the conversation if the user types 'exit'
            if message.lower() in ("exit", "quit"):
                print("Exiting conversation...")
                break
        
            # Send the message to the Flask app
            response =  engine.send_message(message, conversation)
            if response:
                # Display the AI's response
                if response.isStream():
                    print(f"ZiVA: ")
                    for content in response.content:
                        print(content) 
                else: 
                    print(f"ZiVA: {response.content}") 
                # Display bubble suggestions (if any)
                if response.bubbles:
                    print("Quick Actions:")
                    for bubble in response.bubbles:
                        print(f"- {bubble.label} ({bubble.type})")
                if conversation.entities:
                    print("Entities:")
                    for entity_key in conversation.entities:
                        print(f"- {entity_key} ({conversation.entities[entity_key]})")
    async def run_async(self, engine: IAsyncAIEngine):
          # Start a new conversation
        conversation_id = input("Chat ID: ")
        conversation = await engine.start_conversation(conversation_id)
        print(f"Started new conversation with ID: {conversation.id}")

        # print(json.dumps(conversation.get_chats_for_prompt(), indent=4, sort_keys=True,))
    
        while True:
            # Get user input
            message = input("You: ")
            # Exit the conversation if the user types 'exit'
            if message.lower() == "exit":
                print("Exiting conversation...")
                break
        
            # Send the message to the Flask app
            response = await engine.send_message(message, conversation)
            if response:
                # Display the AI's response
                if response.isStream():
                    print(f"ZiVA: ")
                    for content in response.content:
                        print(content) 
                else: 
                    print(f"ZiVA: {response.content}") 
                # Display bubble suggestions (if any)
                if response.bubbles:
                    print("Quick Actions:")
                    for bubble in response.bubbles:
                        print(f"- {bubble.label} ({bubble.type})")
                if conversation.entities:
                    print("Entities:")
                    for entity_key in conversation.entities:
                        print(f"- {entity_key} ({conversation.entities[entity_key]})")
