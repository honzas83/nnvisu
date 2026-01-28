const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 800;

// State
let ws = null;
let points = [];
let isTraining = false;
let currentEpoch = 0;
let currentLoss = 0;
let currentClass = 0;

// Elements
const canvas = document.getElementById('viz-canvas');
const ctx = canvas.getContext('2d');
const statusDiv = document.getElementById('status');
const metricsDiv = document.getElementById('metrics');

// Offscreen canvas for map
let mapCanvas = document.createElement('canvas');
mapCanvas.width = 50;
mapCanvas.height = 50;
let mapCtx = mapCanvas.getContext('2d');
let mapData = null;

// UI Handlers
document.getElementById('btn-class-0').onclick = () => setClass(0);
document.getElementById('btn-class-1').onclick = () => setClass(1);
document.getElementById('btn-class-2').onclick = () => setClass(2);
document.getElementById('btn-clear').onclick = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'CLEAR_POINTS' }));
    }
    points = []; 
    mapData = null;
};
document.getElementById('btn-start').onclick = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'START_TRAINING', payload: { learning_rate: 0.01 } }));
    }
};
document.getElementById('btn-stop').onclick = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'STOP_TRAINING' }));
    }
};

const archInput = document.getElementById('arch-input');

function getArchitecture() {
    const val = archInput.value.trim();
    // Validate: "10-5", "10", etc. Only numbers and hyphens.
    if (!/^\d+(-\d+)*$/.test(val)) {
        alert("Invalid format! Use numbers separated by hyphens (e.g. 10-5).");
        return null;
    }
    return val.split('-').map(Number);
}

function resetModel() {
    const hiddenLayers = getArchitecture();
    if (!hiddenLayers) return;

    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ 
            type: 'RESET_MODEL',
            payload: { hidden_layers: hiddenLayers }
        }));
    }
    mapData = null;
    statusDiv.textContent = 'Status: Model Reset';
    metricsDiv.textContent = 'Epoch: 0 | Loss: 0.0000';
}

document.getElementById('btn-reset').onclick = resetModel;

archInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        resetModel();
        archInput.blur();
    }
});
archInput.addEventListener('blur', () => {
   // Optional: Auto-reset on blur might be annoying if accidental. 
   // Spec says: "Enter key press or when the input field loses focus (blur)"
   // Let's implement it as requested.
   resetModel();
});

canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / CANVAS_WIDTH * 2 - 1; 
    const y = -((e.clientY - rect.top) / CANVAS_HEIGHT * 2 - 1); 
    
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'ADD_POINT',
            payload: { x, y, label: currentClass }
        }));
    }
});

function setClass(cls) {
    currentClass = cls;
    document.querySelectorAll('.class-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`btn-class-${cls}`).classList.add('active');
}

function connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        statusDiv.textContent = 'Status: Connected';
        console.log('Connected to WS');
    };

    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        handleMessage(message);
    };

    ws.onclose = () => {
        statusDiv.textContent = 'Status: Disconnected';
        setTimeout(connect, 2000); // Reconnect
    };
}

function handleMessage(message) {
    if (message.type === 'ADD_POINT') {
        points.push(message.payload);
    } else if (message.type === 'CLEAR_POINTS') {
        points = [];
        mapData = null;
    } else if (message.type === 'TRAINING_STATUS') {
        isTraining = message.payload.is_training;
        currentEpoch = message.payload.epoch;
        currentLoss = message.payload.loss;
        
        statusDiv.textContent = isTraining ? 'Status: Training...' : 'Status: Idle';
        metricsDiv.textContent = `Epoch: ${currentEpoch} | Loss: ${currentLoss.toFixed(4)}`;
        
        document.getElementById('btn-start').disabled = isTraining;
        document.getElementById('btn-stop').disabled = !isTraining;
    } else if (message.type === 'MAP_UPDATE') {
        const { width, height, data } = message.payload;
        const binaryString = atob(data);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        
        const imgData = mapCtx.createImageData(width, height);
        for (let i = 0; i < len; i++) {
            const cls = bytes[i];
            const offset = i * 4;
            if (cls === 0) {
                imgData.data[offset] = 52; imgData.data[offset+1] = 152; imgData.data[offset+2] = 219; imgData.data[offset+3] = 100; // Blue
            } else if (cls === 1) {
                imgData.data[offset] = 230; imgData.data[offset+1] = 126; imgData.data[offset+2] = 34; imgData.data[offset+3] = 100; // Orange
            } else {
                imgData.data[offset] = 231; imgData.data[offset+1] = 76; imgData.data[offset+2] = 60; imgData.data[offset+3] = 100; // Red
            }
        }
        mapCtx.putImageData(imgData, 0, 0);
        createImageBitmap(mapCanvas).then(bmp => {
            mapData = bmp;
        });
    }
}

function render() {
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    ctx.fillStyle = "#f9f9f9";
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    if (mapData) {
        ctx.drawImage(mapData, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    }

    ctx.strokeStyle = '#ddd';
    ctx.beginPath();
    ctx.moveTo(CANVAS_WIDTH/2, 0); ctx.lineTo(CANVAS_WIDTH/2, CANVAS_HEIGHT);
    ctx.moveTo(0, CANVAS_HEIGHT/2); ctx.lineTo(CANVAS_WIDTH, CANVAS_HEIGHT/2);
    ctx.stroke();

    for (const p of points) {
        const screenX = (p.x + 1) / 2 * CANVAS_WIDTH;
        const screenY = (-p.y + 1) / 2 * CANVAS_HEIGHT; 

        ctx.beginPath();
        ctx.arc(screenX, screenY, 5, 0, 2 * Math.PI);
        if (p.label === 0) ctx.fillStyle = '#3498db';
        else if (p.label === 1) ctx.fillStyle = '#e67e22';
        else ctx.fillStyle = '#e74c3c';
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.stroke();
    }
    
    requestAnimationFrame(render);
}

// Init
connect();
requestAnimationFrame(render);