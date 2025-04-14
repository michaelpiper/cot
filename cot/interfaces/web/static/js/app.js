
const chatbot = {
    name: "CoT",
    avatar: "/assets/logo.png"
}

// Initialize Framework7 App
const app = new Framework7({
    el: '#app',
    theme: 'md',
});
window.app = app
// Initialize Messages Component
const messages = app.messages.create({
    el: '.messages-content',
    scrollMessages: true,
    autoLayout: true,
});
// Get DOM Elements
const pageContent = document.querySelector('.page-content');
const messagesContent = document.querySelector('.messages-content');
const messageInput = document.querySelector('.messagebar-textarea');
const sendMessageButton = document.querySelector('.send-message');

// Generate a unique session ID (for demo purposes)
const sessionId = `session-${Math.random().toString(36).substr(2, 9)}`;
// Handle Button Clicks
function handleButtonClick(value) {
    // Simulate sending the button value as user input
    messageInput.value = value;
    sendMessageButton.click();
}
function convertNewlinesToMarkdown(text) {
    return text.replace(/\n/g, '  \n');
}
  
function convertNewlinesToHtml(text) {
    return text.replace(/\n/g, ' <br/>');
}
// Markdown renderer with sanitization
function renderMarkdown(content) {
    const unsafeHtml = marked.parse(content);
    return DOMPurify.sanitize(unsafeHtml, {
        ALLOWED_TAGS: ['p', 'strong', 'em', 'a', 'br', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'code'],
        ALLOWED_ATTR: ['href', 'class']
    });
}

// Helper Function to Add Messages
function addMessage(text, type = 'received', blockId = null) {
    const htmlContent = renderMarkdown(text);

    messages.addMessage({
        text: htmlContent,
        type: type, // 'sent' or 'received'
        day: !messages.messages.length || type === 'received' ? 'Today' : false,
        blockId: blockId, // Store blockId for tracking
    });
}
// Reliable scroll function
function scrollToBottom(animated = true) {
    setTimeout(() => {
        pageContent.scroll(pageContent.scrollWidth, pageContent.scrollHeight);
    }, 50);

}

async function onSendMessageButtonClicked(){
    const userInput = messageInput.value.trim();
    if (!userInput) return;

    // Add User's Message to Chat
    addMessage(convertNewlinesToMarkdown(userInput), 'sent');

    // Clear Input Field
    messageInput.value = '';
    messageInput.style.height=''
    messages.showTyping({
        header: chatbot.name + ' is typing',
        avatar: chatbot.avatar
    });
    setTimeout(() => scrollToBottom(true), 1000)
    try {
        // Send the user input to the server
        const response = await fetch(`http://localhost:4000/chat`, {
            body: JSON.stringify({
                "message": userInput,
                "conversation_id": sessionId
            }),
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });
        const data = await response.json();
        // Process the server response
        if (data.type === "text") {
            // Add received text message
            addMessage(convertNewlinesToHtml(data.content), 'received', data.blockId);
        } else if (data.type === "image" || data.type === "attachment") {
            // Add image or attachment
            addMessage(`<img src="${data.content}" alt="Attachment" style="max-width: 100%;">`, 'received', data.blockId);
        }
        messages.hideTyping()

        // Add buttons if present
        if (data.bubbles && data.bubbles.length > 0) {
            const buttonContainer = document.createElement('div');
            buttonContainer.className = 'button-container';
            data.bubbles.forEach((bubble) => {
                if (bubble.type === "chip") {
                    const chip = document.createElement('div');
                    chip.className = "chip chip-outline"
                    chip.style.maxWidth = "230px"
                    chip.style.margin = "0.2rem"
                    const label = document.createElement('div');
                    label.className = "chip-label"
                    label.textContent = bubble.label;
                    chip.appendChild(label);
                    chip.onclick = () => handleButtonClick(bubble.value); // Handle button clicks
                    buttonContainer.appendChild(chip);
                } else {
                    const button = document.createElement('button');
                    if (bubble.type === "button") {
                        button.className = 'button button-small button-tonal button-round';
                    }
                    else if (bubble.type === "text") {
                        button.className = 'button button-small button-outline button-round';
                    }
                    else if (bubble.type === "link") {
                        button.className = 'button button-small button-round mx-1';
                    }
                    button.style.width = "130px"
                    button.textContent = bubble.label;
                    button.onclick = () => handleButtonClick(bubble.label); // Handle button clicks
                    buttonContainer.appendChild(button);
                }


            });
            messagesContent.appendChild(buttonContainer);
        }
        setTimeout(() => scrollToBottom(true), 1)
    } catch (error) {
        console.error('Error sending message:', error);
        messages.hideTyping()
        addMessage('An error occurred while processing your request.', 'received');
    }
}
// Handle User Input and Send to Endpoint
sendMessageButton.addEventListener('click', onSendMessageButtonClicked);

// Example Initial Message from Server
addMessage('Hello! How can I assist you today?', 'received');