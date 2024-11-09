function redirectToStreamlit() {
    // Change this URL to the link of your deployed Streamlit app
    window.location.href = 'http://localhost:8501'; // Replace with your Streamlit app URL
}


function sendChatMessage() {
    let userInput = document.getElementById('chatbot-input').value;
    let chatbotMessages = document.getElementById('chatbot-messages');

    if (userInput.trim() === '') return;

    // User message
    let userMessage = document.createElement('div');
    userMessage.innerHTML = `<strong>You:</strong> ${userInput}`;
    chatbotMessages.appendChild(userMessage);

    // Simulate bot response delay
    setTimeout(() => {
        // Bot response
        let botMessage = document.createElement('div');
        if (userInput.toLowerCase().includes('status')) {
            botMessage.innerHTML = `<strong>FINSERVE Bot:</strong> You can check your loan status in the Admin Dashboard.`;
        } else if (userInput.toLowerCase().includes('apply')) {
            botMessage.innerHTML = `<strong>FINSERVE Bot:</strong> You can apply for a loan on the Apply Loan page.`;
        } else {
            botMessage.innerHTML = `<strong>FINSERVE Bot:</strong> I can help with loan applications and status inquiries.`;
        }

        chatbotMessages.appendChild(botMessage);

        // Scroll to the bottom
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

        // Clear input field and refocus
        document.getElementById('chatbot-input').value = '';
        document.getElementById('chatbot-input').focus();
    }, 500); // Simulate a 500ms delay
}
