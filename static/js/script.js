let awaitingAnswer = false;
let pendingQuestion = "";

document.getElementById('send-btn').addEventListener('click', sendMessage);

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== "") {
        addMessageToChat("You", userInput);

        // If the bot is waiting for an answer (learning mode)
        if (awaitingAnswer) {
            learnNewResponse(pendingQuestion, userInput);
            awaitingAnswer = false;  // Reset learning mode
        } else {
            fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userInput }),
            })
            .then(response => response.json())
            .then(data => {
                addMessageToChat("Bot", data.response);

                // Check if the bot asks to learn a new answer
                if (data.response === "I don't know the answer. Can you teach me?") {
                    awaitingAnswer = true;  // Activate learning mode
                    pendingQuestion = userInput;  // Store the question for which the answer is awaited
                }
            });
        }

        // Clear input field
        document.getElementById('user-input').value = "";
    }
}

function addMessageToChat(sender, message) {
    const chatLog = document.getElementById('chat-log');
    const messageElement = document.createElement('div');
    messageElement.textContent = `${sender}: ${message}`;
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight;
}

function learnNewResponse(question, answer) {
    fetch('/learn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question, answer: answer }),
    })
    .then(response => response.json())
    .then(data => {
        addMessageToChat("Bot", data.response);
    });
}
