import { StateManager } from './state_manager.js';

const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 800;

const stateManager = new StateManager();
let currentState = stateManager.loadState();

// Local copy for rendering/logic
let points = currentState.data;
let config = currentState.config;
let weights = currentState.weights;

let ws = null;
let isTraining = false;
let currentEpoch = 0; 
let currentLoss = 0;
let currentClass = 0;

const canvas = document.getElementById('viz-canvas');
const ctx = canvas.getContext('2d');
const statusDiv = document.getElementById('status');
const metricsDiv = document.getElementById('metrics');

let mapCanvas = document.createElement('canvas');
mapCanvas.width = 50;
mapCanvas.height = 50;
let mapCtx = mapCanvas.getContext('2d');
let mapData = null;

// Inputs
const archInput = document.getElementById('arch-input');
if (config.architecture) {
    archInput.value = config.architecture.join('-');
}

// UI Handlers
document.getElementById('btn-class-0').onclick = () => setClass(0);
document.getElementById('btn-class-1').onclick = () => setClass(1);
document.getElementById('btn-class-2').onclick = () => setClass(2);

document.getElementById('btn-clear').onclick = () => {
    points = [];
    stateManager.saveData(points);
    mapData = null;
    render();
};

document.getElementById('btn-start').onclick = () => {
    if (!isTraining) {
        isTraining = true;
        updateUIStatus();
        runTrainingLoop();
    }
};

document.getElementById('btn-stop').onclick = () => {
    isTraining = false;
    updateUIStatus();
};

document.getElementById('btn-reset').onclick = resetModel;

function resetModel() {
    isTraining = false;
    weights = null;
    stateManager.saveWeights(null);
    mapData = null;
    currentEpoch = 0;
    currentLoss = 0;
    
    const val = archInput.value.trim();
    if (/^\d+(-\d+)*$/.test(val)) {
        config.architecture = val.split('-').map(Number);
        stateManager.saveConfig(config);
    }
    
    updateUIStatus();
    statusDiv.textContent = 'Status: Model Reset';
    metricsDiv.textContent = 'Steps: 0 | Loss: N/A';
}

archInput.addEventListener('blur', resetModel);
archInput.addEventListener('keydown', (e) => { 
    if(e.key === 'Enter') { 
        resetModel(); 
        archInput.blur(); 
    }
});

canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / CANVAS_WIDTH * 2 - 1; 
    const y = -((e.clientY - rect.top) / CANVAS_HEIGHT * 2 - 1); 
    
    points.push({ x, y, label: currentClass });
    stateManager.saveData(points);
});

function setClass(cls) {
    currentClass = cls;
    document.querySelectorAll('.class-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`btn-class-${cls}`).classList.add('active');
}

function updateUIStatus() {
    statusDiv.textContent = isTraining ? 'Status: Training...' : 'Status: Idle';
    metricsDiv.textContent = `Steps: ${currentEpoch} | Loss: ${currentLoss.toFixed(4)}`;
    document.getElementById('btn-start').disabled = isTraining;
    document.getElementById('btn-stop').disabled = !isTraining;
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
        setTimeout(connect, 2000);
    };
}

function handleMessage(message) {
    if (message.type === 'step_result') {
        weights = message.model;
        stateManager.saveWeights(weights);
        
        currentLoss = message.metrics.loss;
        currentEpoch++;
        
        updateUIStatus();
        
        if (isTraining) {
            runTrainingLoop();
        }
    } else if (message.type === 'map_update') {
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
                imgData.data[offset] = 52; imgData.data[offset+1] = 152; imgData.data[offset+2] = 219; imgData.data[offset+3] = 100;
            } else if (cls === 1) {
                imgData.data[offset] = 230; imgData.data[offset+1] = 126; imgData.data[offset+2] = 34; imgData.data[offset+3] = 100;
            } else {
                imgData.data[offset] = 231; imgData.data[offset+1] = 76; imgData.data[offset+2] = 60; imgData.data[offset+3] = 100;
            }
        }
        mapCtx.putImageData(imgData, 0, 0);
        createImageBitmap(mapCanvas).then(bmp => {
            mapData = bmp;
        });
    }
}

function runTrainingLoop() {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    if (!isTraining) return;

    const payload = {
        type: 'train_step',
        config: config,
        model: weights || { weights: [], biases: [] },
        data: points
    };
    ws.send(JSON.stringify(payload));
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

connect();
requestAnimationFrame(render);
