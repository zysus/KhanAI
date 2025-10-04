// Khan AI - Chat JavaScript

let currentMode = "normal";
let chatHistory = [];

async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    addMessage(message, 'user');
    input.value = '';
    
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                mode: currentMode
            })
        });
        
        const data = await response.json();
        
        removeTypingIndicator();
        
        if (data.status === 'success') {
            addMessage(data.response, 'khan');
            
            chatHistory.push({
                user: message,
                khan: data.response,
                mode: data.mode,
                timestamp: new Date().toISOString()
            });
            
            if (data.feedback_prompt) {
                setTimeout(() => showFeedbackModal(), 2000);
            }
        } else {
            addMessage('Error al procesar el mensaje', 'system');
        }
    } catch (error) {
        removeTypingIndicator();
        addMessage('Error de conexión con Khan', 'system');
        console.error('Error:', error);
    }
}

function addMessage(text, type) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const formattedText = formatMessage(text);
    contentDiv.innerHTML = formattedText;
    
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function formatMessage(text) {
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    text = text.replace(/`(.*?)`/g, '<code>$1</code>');
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message khan-message typing-indicator';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = '<div class="message-content"><p>Khan está pensando...</p></div>';
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function toggleMode() {
    const modeBtn = document.getElementById('modeBtn');
    const modeIcon = document.getElementById('modeIcon');
    const modeText = document.getElementById('modeText');
    
    if (currentMode === 'normal') {
        currentMode = 'serio';
        modeIcon.textContent = '🎯';
        modeText.textContent = 'Modo Serio';
        modeBtn.style.borderColor = '#ff0055';
    } else {
        currentMode = 'normal';
        modeIcon.textContent = '🤖';
        modeText.textContent = 'Modo Normal';
        modeBtn.style.borderColor = '#00ffff';
    }
}

function toggleHistory() {
    const sidebar = document.getElementById('historySidebar');
    sidebar.classList.toggle('active');
    
    if (sidebar.classList.contains('active')) {
        loadHistory();
    }
}

async function loadHistory() {
    const historyContent = document.getElementById('historyContent');
    historyContent.innerHTML = '<p class="loading">Cargando historial...</p>';
    
    try {
        const response = await fetch('/api/history?limit=20');
        const data = await response.json();
        
        if (data.status === 'success' && data.history.length > 0) {
            historyContent.innerHTML = '';
            data.history.forEach(item => {
                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                historyItem.innerHTML = `
                    <div class="history-message">
                        <strong>Usuario:</strong> ${item.message.substring(0, 50)}...
                    </div>
                    <div class="history-response">
                        <strong>Khan:</strong> ${item.response.substring(0, 50)}...
                    </div>
                    <div class="history-meta">
                        ${new Date(item.timestamp).toLocaleString()}
                    </div>
                `;
                historyContent.appendChild(historyItem);
            });
        } else {
            historyContent.innerHTML = '<p class="loading">No hay historial disponible</p>';
        }
    } catch (error) {
        historyContent.innerHTML = '<p class="loading">Error cargando historial</p>';
        console.error('Error:', error);
    }
}

function showFeedbackModal() {
    const modal = document.getElementById('feedbackModal');
    modal.classList.add('active');
}

function closeFeedbackModal() {
    const modal = document.getElementById('feedbackModal');
    modal.classList.remove('active');
}

async function submitFeedback(score) {
    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                score: score,
                comment: null
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            addMessage(`Gracias por tu feedback (${score}/10). Khan aprende de ti.`, 'system');
        }
    } catch (error) {
        console.error('Error enviando feedback:', error);
    }
    
    closeFeedbackModal();
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('messageInput').focus();
    
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (confirm('¿Limpiar el chat actual?')) {
                document.getElementById('chatMessages').innerHTML = '';
                addMessage('Chat limpiado. Khan está listo para continuar.', 'system');
            }
        }
        
        if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
            e.preventDefault();
            toggleHistory();
        }
    });
    
    document.getElementById('feedbackModal').addEventListener('click', (e) => {
        if (e.target.id === 'feedbackModal') {
            closeFeedbackModal();
        }
    });
});
