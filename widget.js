// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // DOM element selection
    const chatToggleButton = document.getElementById('chat-toggle-button');
    const chatWidget = document.getElementById('chat-widget');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const messageContainer = document.getElementById('message-container');

    // Toggle button click handler - opens/closes the chat widget
    chatToggleButton.addEventListener('click', function() {
        chatWidget.classList.toggle('open');
        
        // Focus on input when widget opens
        if (chatWidget.classList.contains('open')) {
            setTimeout(() => {
                messageInput.focus();
            }, 300); // Wait for animation to complete
        }
    });

    // Form submission handler
    chatForm.addEventListener('submit', function(e) {
        // Prevent default form submission (page reload)
        e.preventDefault();
        
        // Get the user's message and trim whitespace
        const userMessage = messageInput.value.trim();
        
        // If message is empty, do nothing
        if (!userMessage) {
            return;
        }

        // Display user's message immediately in the UI
        addMessageToUI(userMessage, 'user');
        
        // Clear the input field
        messageInput.value = '';
        
        // Send message to backend
        sendMessageToBackend(userMessage);
    });

    /**
     * Helper function to add a message to the UI
     * @param {string} text - The message text to display
     * @param {string} sender - Either 'user' or 'bot' to determine styling
     */
    function addMessageToUI(text, sender) {
        // Create a new div element for the message bubble
        const messageDiv = document.createElement('div');
        
        // Apply the correct CSS classes based on sender
        messageDiv.classList.add('message-bubble');
        if (sender === 'user') {
            messageDiv.classList.add('user-message');
        } else {
            messageDiv.classList.add('bot-message');
        }
        
        // Set the message text
        messageDiv.textContent = text;
        
        // Append the message to the message container
        messageContainer.appendChild(messageDiv);
        
        // Automatically scroll to the bottom to show the latest message
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    /**
     * Helper function to send message to the backend API
     * @param {string} message - The user's message to send to the backend
     */
    async function sendMessageToBackend(message) {
        try {
            // Make POST request to the FastAPI backend
            const response = await fetch('http://127.0.0.1:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            // Check if the response is successful
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Parse the JSON response
            const data = await response.json();
            
            // Extract the bot's reply from the response
            const botReply = data.reply;
            
            // Display the bot's response in the UI
            addMessageToUI(botReply, 'bot');
            
        } catch (error) {
            // Log any network or parsing errors to the console
            console.error('Error communicating with backend:', error);
            
            // Display an error message to the user
            addMessageToUI('Sorry, I encountered an error. Please try again.', 'bot');
        }
    }
});
