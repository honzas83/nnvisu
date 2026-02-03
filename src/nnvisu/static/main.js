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
let currentTool = 'draw'; // 'draw' or 'erase'

// Training History
let history = []; // Array of { epoch, mapData, loss }
let recordingInterval = 10;
const MAX_HISTORY = 256;

const CLASS_COLORS = [
    '#3498db', // Blue
    '#e67e22', // Orange
    '#e74c3c', // Red
    '#9b59b6', // Purple
    '#2ecc71', // Green
    '#f1c40f', // Yellow
    '#795548', // Brown
    '#34495e'  // Navy
];

const canvas = document.getElementById('viz-canvas');
const ctx = canvas.getContext('2d');
const statusDiv = document.getElementById('status');
const metricsDiv = document.getElementById('metrics');
const historySeekbar = document.getElementById('history-seekbar');

let mapCanvas = document.createElement('canvas');
mapCanvas.width = 100;
mapCanvas.height = 100;
let mapCtx = mapCanvas.getContext('2d');
let mapData = null;

// Mouse tracking for eraser cursor
let mousePos = { x: 0, y: 0 };
const ERASER_RADIUS = 20;

// Inputs
const archInput = document.getElementById('arch-input');
if (config.architecture) {
    archInput.value = config.architecture.join('-');
}

const activationSelect = document.getElementById('activation-select');
activationSelect.value = config.activation || 'tanh';

const optimizerSelect = document.getElementById('optimizer-select');
optimizerSelect.value = config.optimizer || 'adam';

const lrInput = document.getElementById('lr-input');
lrInput.value = config.learningRate;

const regInput = document.getElementById('reg-input');
regInput.value = config.regularization || 0;

const batchInput = document.getElementById('batch-input');
batchInput.value = config.batchSize || 0;

const dropoutInput = document.getElementById('dropout-input');
dropoutInput.value = config.dropout || 0;

const advancedOptions = document.getElementById('advanced-options');
// Restore expanded state
const isExpanded = localStorage.getItem('nnvisu_advanced_expanded') === 'true';
if (isExpanded) {
    advancedOptions.open = true;
}

// Persist expanded state
advancedOptions.addEventListener('toggle', () => {
    localStorage.setItem('nnvisu_advanced_expanded', advancedOptions.open);
});

function resetAdvancedToDefaults() {
    // Original defaults before Advanced introduction
    config.activation = 'tanh';
    config.optimizer = 'adam';
    config.learningRate = 0.01;
    config.regularization = 0;
    config.batchSize = 0;
    config.dropout = 0;
    
    // Update UI
    activationSelect.value = config.activation;
    optimizerSelect.value = config.optimizer;
    lrInput.valueAsNumber = config.learningRate;
    regInput.valueAsNumber = config.regularization;
    batchInput.valueAsNumber = config.batchSize;
    dropoutInput.valueAsNumber = config.dropout;
    
    stateManager.saveConfig(config);
    updateConfig();
    resetModel(); // Reset weights when returning to base configuration
}

document.getElementById('btn-reset-advanced-main').onclick = resetAdvancedToDefaults;
document.getElementById('btn-reset-advanced-panel').onclick = resetAdvancedToDefaults;

// UI Handlers
function updateConfig() {
    config.activation = activationSelect.value;
    config.optimizer = optimizerSelect.value;
    config.learningRate = parseFloat(lrInput.value) || 0.01;
    config.regularization = parseFloat(regInput.value) || 0;
    config.batchSize = parseInt(batchInput.value) || 0;
    config.dropout = parseFloat(dropoutInput.value) || 0;
    stateManager.saveConfig(config);
    
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'update_config',
            payload: config
        }));
    }
}

[activationSelect, optimizerSelect, lrInput, regInput, batchInput, dropoutInput].forEach(el => {
    el.addEventListener('change', () => {
        if (el === activationSelect) {
            resetModel();
        } else {
            if (isTraining) {
                toggleTraining();
            }
            updateConfig();
        }
    });
});

function initPalette() {
    const palette = document.getElementById('palette');
    CLASS_COLORS.forEach((color, idx) => {
        const swatch = document.createElement('div');
        swatch.className = 'swatch';
        swatch.style.backgroundColor = color;
        swatch.title = `Class ${idx}`;
        swatch.onclick = () => setClass(idx);
        if (idx === 0) swatch.classList.add('active');
        palette.appendChild(swatch);
    });
}
initPalette();

document.getElementById('btn-eraser').onclick = () => setTool('erase');

document.getElementById('btn-clear').onclick = () => {
    points = [];
    stateManager.saveData(points);
    mapData = null;
    history = [];
    updateHistoryUI();
    sendDataUpdate();
    render();
};

document.getElementById('btn-play-pause').onclick = toggleTraining;

document.getElementById('btn-reset').onclick = resetModel;

function toggleTraining() {
    isTraining = !isTraining;
    updateUIStatus();
    
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    
    if (isTraining) {
        ws.send(JSON.stringify({ type: 'start_training' }));
    } else {
        ws.send(JSON.stringify({ type: 'stop_training' }));
    }
}

function resetModel() {
    isTraining = false;
    weights = null;
    stateManager.saveWeights(null);
    mapData = null;
    currentEpoch = 0;
    currentLoss = 0;
    history = [];
    recordingInterval = 10;
    updateHistoryUI();
    
    const val = archInput.value.trim();
    if (/^\d+(-\d+)*$/.test(val)) {
        config.architecture = val.split('-').map(Number);
        stateManager.saveConfig(config);
    }
    
    updateUIStatus();
    statusDiv.textContent = 'Status: Model Reset';
    metricsDiv.textContent = 'Steps: 0 | Loss: N/A';
    
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'reset' }));
        updateConfig();
    }
}

archInput.addEventListener('blur', resetModel);
archInput.addEventListener('keydown', (e) => { 
    if(e.key === 'Enter') { 
        resetModel(); 
        archInput.blur(); 
    }
});

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mousePos.x = e.clientX - rect.left;
    mousePos.y = e.clientY - rect.top;
});

canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / CANVAS_WIDTH * 2 - 1; 
    const y = -((e.clientY - rect.top) / CANVAS_HEIGHT * 2 - 1); 
    
    if (currentTool === 'draw') {
        points.push({ x, y, label: currentClass });
    } else {
        // Erase: Remove points within radius
        const radius = ERASER_RADIUS / CANVAS_WIDTH * 2;
        points = points.filter(p => {
            const dx = p.x - x;
            const dy = p.y - y;
            return Math.sqrt(dx*dx + dy*dy) > radius;
        });
    }
    stateManager.saveData(points);
    sendDataUpdate();
});

function sendDataUpdate() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'update_data',
            data: points
        }));
    }
}

function setClass(cls) {
    currentClass = cls;
    currentTool = 'draw';
    document.querySelectorAll('.swatch').forEach((s, idx) => {
        s.classList.toggle('active', idx === cls);
    });
    document.getElementById('btn-eraser').classList.remove('active');
}

function setTool(tool) {
    currentTool = tool;
    if (tool === 'erase') {
        document.querySelectorAll('.swatch').forEach(s => s.classList.remove('active'));
        document.getElementById('btn-eraser').classList.add('active');
    }
}

function updateUIStatus() {
    const playBtn = document.getElementById('btn-play-pause');
    playBtn.textContent = isTraining ? '⏸ Pause' : '▶ Train';
    playBtn.style.background = isTraining ? '#e74c3c' : '#2ecc71';
    
    statusDiv.textContent = isTraining ? 'Status: Training...' : 'Status: Idle';
    metricsDiv.textContent = `Steps: ${currentEpoch} | Loss: ${currentLoss.toFixed(4)}`;

    // Add class for pulse animation
    document.querySelector('.status-integration').classList.toggle('training-active', isTraining);
}

function updateHistoryUI() {
    historySeekbar.max = Math.max(0, history.length - 1);
    if (isTraining || history.length > 0) {
        historySeekbar.value = history.length - 1;
    }
}

function connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const path = window.location.pathname.replace(/\/$/, '');
    const wsUrl = `${protocol}//${window.location.host}${path}/ws`;
    
    ws = new WebSocket(wsUrl);
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
        statusDiv.textContent = 'Status: Connected';
        console.log('Connected to WS');
        // Sync initial state
        updateConfig();
        sendDataUpdate();
    };

    ws.onmessage = (event) => {
        if (event.data instanceof ArrayBuffer) {
            handleBinaryMessage(event.data);
        } else {
            const message = JSON.parse(event.data);
            handleMessage(message);
        }
    };

    ws.onclose = () => {
        statusDiv.textContent = 'Status: Disconnected';
        setTimeout(connect, 2000);
    };
}

function handleBinaryMessage(buffer) {
    const view = new DataView(buffer);
    const type = view.getUint8(0);
    
    if (type === 0x01) { // Map Update
        const width = view.getUint16(1, true); // Little endian
        const height = view.getUint16(3, true);
        
        const headerSize = 5;
        const rgbData = new Uint8Array(buffer, headerSize);
        
        if (mapCanvas.width !== width || mapCanvas.height !== height) {
            mapCanvas.width = width;
            mapCanvas.height = height;
            mapCtx = mapCanvas.getContext('2d');
        }
        
        const imgData = mapCtx.createImageData(width, height);
        // data is RGB (3 bytes), imgData is RGBA (4 bytes)
        const len = rgbData.length;
        for (let i = 0; i < len / 3; i++) {
            const pixelIdx = i * 3;
            const offset = i * 4;
            imgData.data[offset] = rgbData[pixelIdx];
            imgData.data[offset+1] = rgbData[pixelIdx+1];
            imgData.data[offset+2] = rgbData[pixelIdx+2];
            imgData.data[offset+3] = 255; // Alpha
        }
        
        mapCtx.putImageData(imgData, 0, 0);
        createImageBitmap(mapCanvas).then(bmp => {
            mapData = bmp;
            if (isTraining && currentEpoch % recordingInterval === 0) {
                recordHistory(bmp, currentEpoch, currentLoss);
            }
        });
    }
}

function handleMessage(message) {
    if (message.type === 'step_result') {
        // Asynchronous update from server
        if (message.model) {
            weights = message.model;
            stateManager.saveWeights(weights);
        }
        
        if (message.metrics) {
            currentLoss = message.metrics.loss;
            // Use server step count for accuracy
            currentEpoch = message.metrics.step || (currentEpoch + 1);
        }
        
        updateUIStatus();
        
    } else if (message.type === 'map_update') {
        const { width, height, format, data } = message.payload;
        
        if (mapCanvas.width !== width || mapCanvas.height !== height) {
            mapCanvas.width = width;
            mapCanvas.height = height;
            mapCtx = mapCanvas.getContext('2d');
        }

        const binaryString = atob(data);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        
        const imgData = mapCtx.createImageData(width, height);
        if (format === 'rgb') {
            for (let i = 0; i < len / 3; i++) {
                const pixelIdx = i * 3;
                const offset = i * 4;
                imgData.data[offset] = bytes[pixelIdx];
                imgData.data[offset+1] = bytes[pixelIdx+1];
                imgData.data[offset+2] = bytes[pixelIdx+2];
                imgData.data[offset+3] = 100;
            }
        } else {
            // Legacy fallback
            for (let i = 0; i < len; i++) {
                const cls = bytes[i];
                const offset = i * 4;
                const color = hexToRgb(CLASS_COLORS[cls] || '#000');
                imgData.data[offset] = color.r;
                imgData.data[offset+1] = color.g;
                imgData.data[offset+2] = color.b;
                imgData.data[offset+3] = 100;
            }
        }
        mapCtx.putImageData(imgData, 0, 0);
        createImageBitmap(mapCanvas).then(bmp => {
            mapData = bmp;
            if (isTraining && currentEpoch % recordingInterval === 0) {
                recordHistory(bmp, currentEpoch, currentLoss);
            }
        });
    } else if (message.type === 'data_generated') {
        points = message.data;
        stateManager.saveData(points);
        // Reset model weights and training state when data changes
        resetModel();
    } else if (message.type === 'config') {
        const { version, author } = message.payload;
        const footerInfo = document.querySelector('.footer-info');
        if (footerInfo) {
            footerInfo.innerHTML = `
                <span class="author">${author}</span>, Department of Cybernetics, University of West Bohemia.
                <br>
                Version: ${version} | <a href="https://github.com/honzas83/nnvisu" target="_blank">Project GitHub</a>
            `;
        }
    } else if (message.type === 'error') {
        console.error('Server error:', message.message);
        statusDiv.textContent = 'Status: Error';
    }
}

function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : { r: 0, g: 0, b: 0 };
}

function recordHistory(bmp, epoch, loss) {
    history.push({ epoch, mapData: bmp, loss });
    if (history.length > MAX_HISTORY) {
        history = history.filter((_, i) => i % 2 === 0);
        recordingInterval *= 2;
    }
    updateHistoryUI();
}

// Generator Handlers
const genClassesInput = document.getElementById('gen-classes');
const generatorButtons = {
    'btn-gen-circles': 'circles',
    'btn-gen-moons': 'moons',
    'btn-gen-blobs': 'blobs',
    'btn-gen-anisotropic': 'anisotropic',
    'btn-gen-varied': 'varied_variance'
};

Object.entries(generatorButtons).forEach(([id, dist]) => {
    const btn = document.getElementById(id);
    if (btn) {
        btn.onclick = () => {
            if (!ws || ws.readyState !== WebSocket.OPEN) return;
            const numClasses = parseInt(genClassesInput.value) || 2;
            ws.send(JSON.stringify({
                type: 'generate_data',
                distribution: dist,
                num_classes: numClasses
            }));
        };
    }
});

historySeekbar.oninput = () => {
    if (isTraining) return;
    const idx = parseInt(historySeekbar.value);
    const snapshot = history[idx];
    if (snapshot) {
        mapData = snapshot.mapData;
        metricsDiv.textContent = `Steps: ${snapshot.epoch} (History) | Loss: ${snapshot.loss.toFixed(4)}`;
    }
};

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

    // Axis Labels
    ctx.fillStyle = '#999';
    ctx.font = '10px Arial';
    ctx.textAlign = 'center';
    // X axis
    ctx.fillText('-1.0', 20, CANVAS_HEIGHT/2 + 15);
    ctx.fillText('0', CANVAS_WIDTH/2 + 8, CANVAS_HEIGHT/2 + 15);
    ctx.fillText('+1.0', CANVAS_WIDTH - 20, CANVAS_HEIGHT/2 + 15);
    // Y axis
    ctx.textAlign = 'left';
    ctx.fillText('+1.0', CANVAS_WIDTH/2 + 5, 15);
    ctx.fillText('-1.0', CANVAS_WIDTH/2 + 5, CANVAS_HEIGHT - 10);

    for (const p of points) {
        const screenX = (p.x + 1) / 2 * CANVAS_WIDTH;
        const screenY = (-p.y + 1) / 2 * CANVAS_HEIGHT; 

        ctx.beginPath();
        ctx.arc(screenX, screenY, 5, 0, 2 * Math.PI);
        ctx.fillStyle = CLASS_COLORS[p.label] || '#333';
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.stroke();
    }

    if (currentTool === 'erase') {
        ctx.beginPath();
        ctx.arc(mousePos.x, mousePos.y, ERASER_RADIUS, 0, 2 * Math.PI);
        ctx.strokeStyle = 'rgba(0,0,0,0.3)';
        ctx.setLineDash([5, 5]);
        ctx.stroke();
        ctx.setLineDash([]);
    }
    
    requestAnimationFrame(render);
}

connect();
requestAnimationFrame(render);