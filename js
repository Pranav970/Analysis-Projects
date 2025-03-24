function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    let chatBox = document.getElementById("chat-box");

    // Display user message
    let userMessage = document.createElement("p");
    userMessage.classList.add("user-message");
    userMessage.textContent = "You: " + userInput;
    chatBox.appendChild(userMessage);

    // Chatbot Responses
    let botReply = getBotResponse(userInput);
    
    let botMessage = document.createElement("p");
    botMessage.classList.add("bot-message");
    botMessage.textContent = "Bot: " + botReply;
    chatBox.appendChild(botMessage);

    // Clear input
    document.getElementById("user-input").value = "";

    // Auto-scroll to the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

// Simple chatbot logic
function getBotResponse(input) {
    input = input.toLowerCase();

    if (input.includes("hello") || input.includes("hi")) {
        return "Hello! How can I assist you today?";
    } else if (input.includes("how are you")) {
        return "I'm just a bot, but I'm doing great! What about you?";
    } else if (input.includes("your name")) {
        return "I am a simple chatbot here to help you!";
    } else if (input.includes("bye")) {
        return "Goodbye! Have a great day!";
    } else {
        return "I'm not sure how to respond to that. Can you ask something else?";
    }
}