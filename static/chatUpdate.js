const username = document.body.getAttribute('data-username');
const socket = new WebSocket(`ws://${window.location.host}/ws/${username}`);
const chatMessages = document.getElementById("chat-messages");
const messageForm = document.getElementById("message-form");
const messageInput = document.getElementById("message");

socket.onmessage = (event) => {
    const message = event.data;
    appendMessageToChat(message);
};

messageForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const message = messageInput.value;
    appendMessageToChat(`${username}:${message}`);
    socket.send(message);
    messageInput.value = "";
});

function appendMessageToChat(message) {
    const messageElement = document.createElement('li');
    messageElement.innerHTML = formatMessage(message);
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatMessage(message) {
    const [username, text] = message.split(":");
    return `<strong>${username}:</strong> ${text}`;
}
