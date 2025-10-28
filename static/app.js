// AI Agent Dashboard - JavaScript

// State
let isProcessing = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 AI Agent Dashboard initialized');

    // Check server health
    checkHealth();

    // Load initial files
    loadFiles();

    // Setup keyboard shortcuts
    setupKeyboardShortcuts();

    // Auto-refresh files every 10 seconds
    setInterval(loadFiles, 10000);
});

// Check server health
async function checkHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();

        const statusElement = document.getElementById('status');

        if (data.status === 'healthy' && data.agent_initialized && data.storage_initialized) {
            statusElement.classList.add('connected');
            statusElement.classList.remove('error');
            statusElement.querySelector('.status-text').textContent = 'Connected';
            console.log('✅ Server healthy');
        } else {
            statusElement.classList.remove('connected');
            statusElement.classList.add('error');
            statusElement.querySelector('.status-text').textContent = 'Not Ready';
            console.warn('⚠️ Server not fully initialized');
        }
    } catch (error) {
        console.error('❌ Health check failed:', error);
        const statusElement = document.getElementById('status');
        statusElement.classList.remove('connected');
        statusElement.classList.add('error');
        statusElement.querySelector('.status-text').textContent = 'Disconnected';
    }
}

// Send message to agent
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (!message || isProcessing) {
        return;
    }

    // Clear input
    input.value = '';

    // Add user message to chat
    addMessageToChat('user', message);

    // Show typing indicator
    const typingId = showTypingIndicator();

    // Disable send button
    isProcessing = true;
    updateSendButton(true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator(typingId);

        if (data.success) {
            // Add agent response
            addMessageToChat('agent', data.response);

            // Refresh files list (in case files were created/modified)
            setTimeout(loadFiles, 1000);
        } else {
            addMessageToChat('agent', `Error: ${data.error || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('❌ Error sending message:', error);
        removeTypingIndicator(typingId);
        addMessageToChat('agent', `Error: Failed to communicate with server`);
    } finally {
        isProcessing = false;
        updateSendButton(false);
        input.focus();
    }
}

// Add message to chat UI
function addMessageToChat(sender, text) {
    const chatContainer = document.getElementById('chatContainer');

    // Remove welcome message if it exists
    const welcomeMessage = chatContainer.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;

    const now = new Date();
    const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    messageDiv.innerHTML = `
        <div class="message-content">
            <span class="message-label">${sender === 'user' ? '👤 You' : '🤖 Agent'}</span>
            ${text}
            <span class="message-time">${timeString}</span>
        </div>
    `;

    chatContainer.appendChild(messageDiv);

    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
    const chatContainer = document.getElementById('chatContainer');

    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message agent';
    typingDiv.id = 'typing-indicator';

    typingDiv.innerHTML = `
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;

    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return 'typing-indicator';
}

// Remove typing indicator
function removeTypingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
}

// Update send button state
function updateSendButton(disabled) {
    const button = document.getElementById('sendButton');
    button.disabled = disabled;

    if (disabled) {
        button.innerHTML = '<span class="spinner"></span>';
    } else {
        button.innerHTML = '<span>Send</span><span class="button-icon">📤</span>';
    }
}

// Clear chat
function clearChat() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.innerHTML = `
        <div class="welcome-message">
            <h3>👋 Welcome!</h3>
            <p>Chat with your AI agent to manage files. Try these commands:</p>
            <ul>
                <li>Create a file called notes.txt with my shopping list</li>
                <li>Read the notes.txt file</li>
                <li>What files do I have?</li>
                <li>Write a report about AI trends to report.txt</li>
            </ul>
        </div>
    `;
}

// Load files from storage
async function loadFiles() {
    try {
        const response = await fetch('/api/files');
        const data = await response.json();

        if (data.success) {
            updateFilesUI(data.files);
        } else {
            console.error('❌ Error loading files:', data.error);
        }
    } catch (error) {
        console.error('❌ Error loading files:', error);
    }
}

// Update files UI
function updateFilesUI(files) {
    const filesList = document.getElementById('filesList');
    const fileCount = document.getElementById('fileCount');
    const totalSize = document.getElementById('totalSize');

    // Update stats
    fileCount.textContent = files.length;

    const totalBytes = files.reduce((sum, file) => sum + (file.size || 0), 0);
    totalSize.textContent = formatFileSize(totalBytes);

    // Clear and populate files list
    if (files.length === 0) {
        filesList.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">📂</span>
                <p>No files yet</p>
                <small>Create files by chatting with the agent</small>
            </div>
        `;
        return;
    }

    filesList.innerHTML = files.map(file => `
        <div class="file-item">
            <div class="file-info">
                <span class="file-icon">${getFileIcon(file.name)}</span>
                <div class="file-details">
                    <div class="file-name">${file.name}</div>
                    <div class="file-meta">
                        ${formatFileSize(file.size || 0)}
                        ${file.last_modified ? '• ' + formatDate(file.last_modified) : ''}
                    </div>
                </div>
            </div>
            <div class="file-actions">
                <button class="icon-btn view" onclick="viewFile('${file.name}')" title="View file">
                    👁️
                </button>
                <button class="icon-btn delete" onclick="deleteFile('${file.name}')" title="Delete file">
                    🗑️
                </button>
            </div>
        </div>
    `).join('');
}

// View file content
async function viewFile(filename) {
    try {
        const response = await fetch(`/api/files/${encodeURIComponent(filename)}`);
        const data = await response.json();

        if (data.success) {
            showFileModal(data.filename, data.content);
        } else {
            alert(`Error: ${data.error || 'Failed to load file'}`);
        }
    } catch (error) {
        console.error('❌ Error viewing file:', error);
        alert('Error: Failed to load file');
    }
}

// Delete file
async function deleteFile(filename) {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/files/${encodeURIComponent(filename)}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            console.log(`✅ Deleted: ${filename}`);
            loadFiles(); // Refresh files list
        } else {
            alert(`Error: ${data.message || 'Failed to delete file'}`);
        }
    } catch (error) {
        console.error('❌ Error deleting file:', error);
        alert('Error: Failed to delete file');
    }
}

// Show file modal
function showFileModal(filename, content) {
    const modal = document.getElementById('fileModal');
    const modalFileName = document.getElementById('modalFileName');
    const modalFileContent = document.getElementById('modalFileContent');

    modalFileName.textContent = filename;
    modalFileContent.textContent = content;

    modal.classList.add('active');
}

// Close modal
function closeModal() {
    const modal = document.getElementById('fileModal');
    modal.classList.remove('active');
}

// Close modal on background click
document.addEventListener('click', (e) => {
    const modal = document.getElementById('fileModal');
    if (e.target === modal) {
        closeModal();
    }
});

// Setup keyboard shortcuts
function setupKeyboardShortcuts() {
    const input = document.getElementById('messageInput');

    input.addEventListener('keydown', (e) => {
        // Send on Enter (without Shift)
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }

        // Clear on Escape
        if (e.key === 'Escape') {
            input.value = '';
        }
    });
}

// Utility: Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';

    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Utility: Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins}m ago`;

    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;

    const diffDays = Math.floor(diffHours / 24);
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString();
}

// Utility: Get file icon
function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();

    const iconMap = {
        'txt': '📄',
        'pdf': '📕',
        'doc': '📘',
        'docx': '📘',
        'xls': '📗',
        'xlsx': '📗',
        'csv': '📊',
        'json': '📋',
        'xml': '📋',
        'html': '🌐',
        'css': '🎨',
        'js': '⚡',
        'py': '🐍',
        'java': '☕',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'png': '🖼️',
        'gif': '🖼️',
        'mp3': '🎵',
        'mp4': '🎬',
        'zip': '📦',
        'rar': '📦',
    };

    return iconMap[ext] || '📄';
}

// Export functions to global scope
window.sendMessage = sendMessage;
window.clearChat = clearChat;
window.loadFiles = loadFiles;
window.viewFile = viewFile;
window.deleteFile = deleteFile;
window.closeModal = closeModal;
