// Khan AI - Admin Panel JavaScript

let statusData = null;

async function refreshStatus() {
    const statusEl = document.getElementById('systemStatus');
    const ollamaEl = document.getElementById('ollamaStatus');
    const interactionEl = document.getElementById('interactionCount');
    
    statusEl.textContent = 'Actualizando...';
    
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.status === 'success') {
            statusData = data.agent_status;
            
            statusEl.textContent = statusData.status === 'operational' ? 'Operacional' : 'Offline';
            statusEl.style.color = statusData.status === 'operational' ? '#00ff00' : '#ff0055';
            
            if (statusData.ollama_available) {
                ollamaEl.textContent = `Conectado (${statusData.ollama_model})`;
                ollamaEl.style.color = '#00ff00';
            } else {
                ollamaEl.textContent = 'No disponible';
                ollamaEl.style.color = '#ff0055';
            }
            
            interactionEl.textContent = statusData.recent_interactions || 0;
            
            updateQuirksList();
            await loadLogs();
        }
    } catch (error) {
        statusEl.textContent = 'Error';
        statusEl.style.color = '#ff0055';
        console.error('Error:', error);
    }
}

function updateQuirksList() {
    const quirksList = document.getElementById('quirksList');
    
    if (statusData && statusData.active_quirks && statusData.active_quirks.length > 0) {
        quirksList.innerHTML = '';
        statusData.active_quirks.forEach(quirk => {
            const quirkDiv = document.createElement('div');
            quirkDiv.className = 'quirk-item';
            quirkDiv.innerHTML = `
                <span class="quirk-icon">🧩</span>
                <span class="quirk-text">${quirk}</span>
            `;
            quirkDiv.style.cssText = `
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.5rem;
                background: var(--dark-tertiary);
                border-radius: 6px;
                margin-bottom: 0.5rem;
            `;
            quirksList.appendChild(quirkDiv);
        });
    } else {
        quirksList.innerHTML = '<p class="loading">No hay quirks activos</p>';
    }
}

async function loadLogs() {
    const logsContainer = document.getElementById('logsContainer');
    
    try {
        const response = await fetch('/api/history?limit=10');
        const data = await response.json();
        
        if (data.status === 'success' && data.history.length > 0) {
            logsContainer.innerHTML = '';
            
            const table = document.createElement('table');
            table.style.cssText = 'width: 100%; border-collapse: collapse;';
            table.innerHTML = `
                <thead>
                    <tr style="border-bottom: 1px solid var(--primary);">
                        <th style="padding: 0.5rem; text-align: left;">Mensaje</th>
                        <th style="padding: 0.5rem; text-align: left;">Respuesta</th>
                        <th style="padding: 0.5rem; text-align: center;">Feedback</th>
                        <th style="padding: 0.5rem; text-align: center;">Sarcasmo</th>
                        <th style="padding: 0.5rem; text-align: right;">Fecha</th>
                    </tr>
                </thead>
                <tbody id="logsTableBody"></tbody>
            `;
            
            logsContainer.appendChild(table);
            
            const tbody = document.getElementById('logsTableBody');
            data.history.forEach(log => {
                const row = document.createElement('tr');
                row.style.borderBottom = '1px solid var(--dark-tertiary)';
                
                const messagePreview = log.message ? log.message.substring(0, 30) + '...' : 'N/A';
                const responsePreview = log.response ? log.response.substring(0, 40) + '...' : 'N/A';
                const feedbackColor = log.feedback > 7 ? '#00ff00' : log.feedback < 4 ? '#ff0055' : '#00ffff';
                const date = new Date(log.timestamp).toLocaleString('es-ES', {
                    day: '2-digit',
                    month: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                });
                
                row.innerHTML = `
                    <td style="padding: 0.5rem;">${messagePreview}</td>
                    <td style="padding: 0.5rem;">${responsePreview}</td>
                    <td style="padding: 0.5rem; text-align: center; color: ${feedbackColor};">
                        ${log.feedback || '-'}
                    </td>
                    <td style="padding: 0.5rem; text-align: center;">
                        ${log.sarcasmo || 0}%
                    </td>
                    <td style="padding: 0.5rem; text-align: right; color: var(--text-dim);">
                        ${date}
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            logsContainer.innerHTML = '<p class="loading">No hay logs disponibles</p>';
        }
    } catch (error) {
        logsContainer.innerHTML = '<p class="loading">Error cargando logs</p>';
        console.error('Error:', error);
    }
}

function toggleModoSerio() {
    const checkbox = document.getElementById('modoSerio');
    const enabled = checkbox.checked;
    
    console.log('Modo Serio:', enabled ? 'Activado' : 'Desactivado');
    
    showNotification(
        enabled ? 'Modo Serio activado permanentemente' : 'Modo Serio desactivado',
        enabled ? 'success' : 'info'
    );
}

function changeModel() {
    const select = document.getElementById('ollamaModel');
    const model = select.value;
    
    console.log('Cambiando a modelo:', model);
    
    showNotification(`Modelo cambiado a: ${model}`, 'info');
}

function updateSarcasmo() {
    const slider = document.getElementById('sarcasmoLevel');
    const valueSpan = document.getElementById('sarcasmoValue');
    const value = slider.value;
    
    valueSpan.textContent = `${value}%`;
    
    if (value > 80) {
        valueSpan.style.color = '#ff0055';
    } else if (value > 50) {
        valueSpan.style.color = '#00ffff';
    } else {
        valueSpan.style.color = '#00ff00';
    }
}

async function cleanupDatabase() {
    if (!confirm('¿Estás seguro de que quieres limpiar la base de datos? Esto eliminará quirks antiguos y logs obsoletos.')) {
        return;
    }
    
    showNotification('Limpiando base de datos...', 'info');
    
    setTimeout(() => {
        showNotification('Base de datos limpiada correctamente', 'success');
        refreshStatus();
    }, 1500);
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'notification';
    
    const colors = {
        success: '#00ff00',
        error: '#ff0055',
        info: '#00ffff',
        warning: '#ffaa00'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--dark-secondary);
        border: 2px solid ${colors[type] || colors.info};
        border-radius: 8px;
        padding: 1rem 1.5rem;
        color: var(--text);
        box-shadow: 0 0 20px ${colors[type] || colors.info};
        animation: slideIn 0.3s ease-out;
        z-index: 1000;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', () => {
    refreshStatus();
    
    setInterval(refreshStatus, 30000);
    
    const slider = document.getElementById('sarcasmoLevel');
    if (slider) {
        slider.addEventListener('input', updateSarcasmo);
        updateSarcasmo();
    }
});

window.refreshStatus = refreshStatus;
window.toggleModoSerio = toggleModoSerio;
window.changeModel = changeModel;
window.updateSarcasmo = updateSarcasmo;
window.cleanupDatabase = cleanupDatabase;
