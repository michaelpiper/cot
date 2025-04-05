
import asyncio

from flask import Flask, jsonify, request
from flask_cors import CORS
from  ..dependencies import engine
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
        r"/chat": {
            "origins": [
                "http://localhost:3000",  # React/Vue dev server
                "https://yourbank.com"    # Production domain
            ],
            "methods": ["POST","OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
# Define the API endpoint
@app.route("/chat", methods=["POST"])
async def chat():
    # Get the input text from the request
    data = request.json
    message = data.get("message") 
    conversation_id = data.get("conversation_id", "")
    conversation = await engine.start_conversation(conversation_id)
    ai_chat = await engine.send_message(message, conversation)
    # Convert Chat object to JSON
    response = {
        "content": ai_chat.content,
        "type": ai_chat.type,
        "blockId": ai_chat.blockId,
        "bubbles": [{"label": b.label, "value": b.value, "type": b.type} for b in ai_chat.bubbles],
    }

    return jsonify(response)

if __name__ == "__main__":
    from . import start_api
    # For development direct execution
    asyncio.run(start_api(app))