# Quickstart: Neural Training Viz

## Prerequisites
- Python 3.11+
- Node.js (Optional, only if using a simple HTTP server for frontend)
- Modern Web Browser

## Setup

1. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the Backend**
   ```bash
   # Starts Tornado server on localhost:8888
   python src/app.py
   ```

3. **Launch the Frontend**
   Since the frontend is static HTML/JS, you can open it directly or serve it.
   ```bash
   # Option A: Python SimpleHTTPServer
   cd frontend/src
   python -m http.server 8000
   # Open http://localhost:8000
   ```

## Usage
1. Click on the canvas to add points (Left Click: Class 0, Right Click or Shift+Click: Class 1).
2. Click "Start Training".
3. Watch the background change colors.
4. Click "Stop" to pause. Add more points to refine.
