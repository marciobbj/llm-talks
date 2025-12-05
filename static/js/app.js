document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const topicInput = document.getElementById('topic-input');
    const startBtn = document.getElementById('start-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const typingIndicator = document.getElementById('typing-indicator');

    let isRunning = false;
    let turnCount = 0;
    const MAX_TURNS = 20;

    function appendMessage(speaker, text, modelName) {
        const msgDiv = document.createElement('div');
        // Clean speaker name for CSS class
        const speakerClass = speaker.replace(/\s+/g, '-');
        msgDiv.className = `message ${speakerClass}`;

        msgDiv.innerHTML = `
            <div class="message-header">${speaker} ${modelName ? `<small>(${modelName})</small>` : ''}</div>
            <div class="message-bubble">${text}</div>
        `;

        // Insert before the typing indicator
        const typingIndicator = document.getElementById('typing-indicator');
        chatContainer.insertBefore(msgDiv, typingIndicator);

        scrollToBottom();
    }

    function scrollToBottom() {
        const typingIndicator = document.getElementById('typing-indicator');

        // Smart scroll: Only scroll if user is already near the bottom
        // or if it's the very start of the conversation
        const threshold = 100; // pixels
        const position = chatContainer.scrollTop + chatContainer.offsetHeight;
        const height = chatContainer.scrollHeight;
        const isNearBottom = position >= height - threshold;

        if (isNearBottom || turnCount === 0) {
            if (typingIndicator) {
                typingIndicator.scrollIntoView({ behavior: 'smooth', block: 'end' });
            } else {
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }
    }

    async function startConversation() {
        const topic = topicInput.value;
        if (!topic) return;

        // UI Reset
        chatContainer.innerHTML = '';
        startBtn.disabled = true;
        topicInput.disabled = true;
        pauseBtn.disabled = false;
        isRunning = true;
        turnCount = 0;

        try {
            const response = await fetch('/api/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic: topic })
            });

            const data = await response.json();

            // Add history (usually just moderator)
            data.history.forEach(msg => {
                appendMessage(msg.speaker, msg.text, msg.model);
            });

            // Start loop
            processTurn();

        } catch (error) {
            console.error('Error starting:', error);
            alert('Failed to start conversation');
            startBtn.disabled = false;
            topicInput.disabled = false;
        }
    }

    async function processTurn() {
        if (!isRunning || turnCount >= MAX_TURNS) {
            stopConversation();
            return;
        }

        typingIndicator.classList.add('active');
        scrollToBottom();

        try {
            const response = await fetch('/api/next', {
                method: 'POST'
            });
            const data = await response.json();

            typingIndicator.classList.remove('active');

            if (data.error) {
                console.error(data.error);
                return;
            }

            appendMessage(data.speaker, data.text, data.model);
            turnCount++;

            // Small delay before next turn for readability
            if (isRunning) {
                setTimeout(processTurn, 1500);
            }

        } catch (error) {
            console.error('Error fetching turn:', error);
            typingIndicator.classList.remove('active');
        }
    }

    function stopConversation() {
        isRunning = false;
        startBtn.disabled = false;
        topicInput.disabled = false;
        pauseBtn.disabled = true;
        typingIndicator.classList.remove('active');
    }

    startBtn.addEventListener('click', startConversation);
    pauseBtn.addEventListener('click', () => {
        isRunning = false; // This will stop the next processTurn call
        pauseBtn.disabled = true;
        startBtn.disabled = false;
    });

    // Clear function
    const clearBtn = document.getElementById('clear-btn');
    clearBtn.addEventListener('click', async () => {
        stopConversation();

        // Remove all message elements but keep the typing indicator
        const messages = chatContainer.querySelectorAll('.message');
        messages.forEach(msg => msg.remove());

        // Reset backend state
        try {
            await fetch('/api/reset', { method: 'POST' });
        } catch (error) {
            console.error('Error resetting:', error);
        }

        turnCount = 0;
    });

    // Export function
    const exportBtn = document.getElementById('export-btn');
    exportBtn.addEventListener('click', () => {
        // Temporarily hide typing indicator for clean screenshot
        const originalDisplay = typingIndicator.style.display;
        typingIndicator.style.display = 'none';

        html2canvas(chatContainer, {
            useCORS: true,
            backgroundColor: '#0013a0ff', // Ensure white background
            windowWidth: chatContainer.scrollWidth,
            windowHeight: chatContainer.scrollHeight
        }).then(canvas => {
            // Restore typing indicator
            typingIndicator.style.display = originalDisplay;

            // Trigger download
            const link = document.createElement('a');
            link.download = `llm-talks-chat-${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.png`;
            link.href = canvas.toDataURL();
            link.click();
        }).catch(err => {
            console.error('Export failed:', err);
            typingIndicator.style.display = originalDisplay;
            alert('Failed to export chat image');
        });
    });
});
