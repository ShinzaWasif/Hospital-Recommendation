document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('chatInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    let input = document.getElementById('chatInput');
    let chatbox = document.getElementById('chatbox');
    if (input.value.trim() !== '') {
        let userMessage = document.createElement('div');
        userMessage.className = "bg-gradient-to-r from-green-400 to-blue-500 text-white p-3 rounded-lg self-end max-w-xs text-right ml-auto";
        userMessage.textContent = input.value;
        chatbox.appendChild(userMessage);
        input.value = '';
        chatbox.scrollTop = chatbox.scrollHeight;
    }
}
