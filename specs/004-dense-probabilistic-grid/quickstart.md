# Quickstart: Dense Probabilistic Grid

## Prerequisites
- Python 3.11+
- Virtual environment activated (`source .venv/bin/activate`)
- Dependencies installed (`pip install -e .`)

## Running the Application

1. **Start the Server**:
   ```bash
   python -m nnvisu.app
   ```

2. **Open the Visualization**:
   - Navigate to `http://localhost:8888` in your browser.

## Verifying the Feature

1. **Check Resolution**:
   - Add a few data points by clicking on the canvas.
   - Click "Start Training".
   - Open Browser Developer Tools -> Network -> WS -> Messages.
   - Look for `map_update` messages.
   - Verify `payload.width` and `payload.height` are `100`.

2. **Verify Color Blending**:
   - Create a scenario with overlapping classes (e.g., place a Blue point near an Orange point).
   - Observe the boundary between the regions.
   - It should be a smooth gradient (blended colors) rather than a jagged line.
