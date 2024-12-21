const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', () => {
    const userMessage = userInput.value;
    if (userMessage) {
        displayMessage('User', userMessage);
        userInput.value = '';
        getResponse(userMessage);
    }
});

function displayMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.innerText = `${sender}: ${message}`;
    chatBox.appendChild(messageElement);
}

function getResponse(userMessage) {
    // Simulate a response from the chatbot
    const botResponse = `You said: ${userMessage}`;
    displayMessage('Chatbot', botResponse);
}
