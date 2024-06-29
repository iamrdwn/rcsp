class WebSocketHandler {
    constructor(url, onMessageCallback) {
        this.ws = new WebSocket(url);
        this.onMessageCallback = onMessageCallback;

        this.ws.onopen = () => {
            console.log('WebSocket connection established');
        };

        this.ws.onmessage = (event) => {
            if (this.onMessageCallback) {
                this.onMessageCallback(event.data);
            }
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        this.ws.onclose = (event) => {
            console.log('WebSocket connection closed:', event);
        };
    }

    sendMessage(message) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(message);
        } else {
            console.error('WebSocket is not open.');
        }
    }

    close() {
        this.ws.close();
    }
}

function initializeWebSocket(url, messageElementId) {
    const messageList = document.getElementById(messageElementId);
    const wsHandler = new WebSocketHandler(url, (message) => {
        let messageElement = document.createElement('li');
        messageElement.textContent = message;
        messageList.appendChild(messageElement);
    });
    return wsHandler;
}

function sendMessage(wsHandler, message) {
    wsHandler.sendMessage(message);
}
