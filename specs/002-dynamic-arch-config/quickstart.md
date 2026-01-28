# Quickstart: Dynamic Architecture Feature

## Prerequisites
- Python 3.11+
- Node.js (optional, for serving frontend if not using Python static files)
- Virtual environment active

## Running the Application

1. **Start Backend**:
   ```bash
   cd backend
   source .venv/bin/activate
   python src/app.py
   ```

2. **Access Frontend**:
   Open `http://localhost:8888` in your browser.

## Verifying the Feature

### 1. Dynamic Architecture
1.  Locate the architecture input box (default "10-5").
2.  Change it to "5-5-5" and press Enter.
3.  Check the server logs; you should see "Model reset with architecture: [5, 5, 5]".
4.  Try training (`Start Training`); verification should show loss decreasing.

### 2. 3rd Class (Red)
1.  Click the "Class 2 (Red)" button (newly added).
2.  Click on the canvas to add red points.
3.  Click "Start Training".
4.  Observe the background heatmap. You should see a red region forming around the red points.
