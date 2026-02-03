# Quickstart: Responsive Layout

## Prerequisites
- Python 3.11+
- Modern browser (Chrome, Firefox, Safari)

## Setup & Run

1. **Install dependencies (CPU-only)**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: This uses the `--extra-index-url` for the PyTorch CPU-only build to avoid downloading the CUDA backend.)*

2. **Run the application**:
   ```bash
   python -m nnvisu
   ```

3. **Access the app**:
   Open `http://localhost:8080` in your browser.

## Verifying Responsive Layout

1. **Wide Mode**:
   - Resize your browser window to a width greater than **1024px**.
   - Observe the two-column layout: toolboxes on the left, canvas on the right.
   - Verify the left column scrolls independently if you have many points or the history is long.
   - Verify the canvas stays fixed in view.

2. **Narrow Mode**:
   - Resize your browser window to a width less than **1024px**.
   - Observe the stacked layout: header and controls on top, canvas below.
   - Verify the canvas scales down to fit the window width.

## Verifying Proxy Fix (Simulated)

1. Open your browser's Developer Tools (F12).
2. Go to the **Console** tab.
3. Verify that the WebSocket connection URL correctly reflects the current page URL (e.g., `ws://localhost:8080/ws`).
4. (Optional) If you have a local reverse proxy (like Nginx), configure it to serve `nnvisu` at a subpath (e.g., `/test/`) and verify the WebSocket still connects to `ws://localhost:8080/test/ws`.

## Verifying Metadata

1. Check the page footer.
2. It should display **Version: 1.0** and **Author: Jan Švec**.
