let sessionId = null;
const chatHistory = document.getElementById('chat-history');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Auto-focus input
messageInput.focus();

// Event Listeners
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function appendMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');

    if (sender === 'bot') {
        // Parse Markdown for bot messages
        div.innerHTML = marked.parse(text);
    } else {
        div.textContent = text;
    }

    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function showTypingIndicator() {
    const div = document.createElement('div');
    div.id = 'typing-indicator';
    div.classList.add('typing-indicator');
    div.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Clear input
    messageInput.value = '';

    // UI Updates
    appendMessage(message, 'user');
    showTypingIndicator();
    sendButton.disabled = true;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Update session ID if established/changed
        if (data.session_id) {
            sessionId = data.session_id;
        }

        removeTypingIndicator();
        appendMessage(data.response, 'bot');

    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        appendMessage("Sorry, I'm having trouble connecting to the Hidden Leaf Village. Please try again later.", 'bot');
    } finally {
        sendButton.disabled = false;
        messageInput.focus();
    }
}
