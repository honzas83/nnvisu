# Quickstart: Optimize Network Training

## Prerequisites

- Standard project requirements (Python 3.11+, etc.)
- **Chrome/Firefox DevTools**: To test network throttling.

## Running the Optimized Version

1.  Start the server:
    ```bash
    python -m src.nnvisu
    ```
2.  Open `http://localhost:8000`.

## Verifying Network Performance

1.  Open the browser's Developer Tools (F12).
2.  Go to the **Network** tab.
3.  Locate the "No throttling" dropdown (usually near the top right of the Network pane).
4.  Select **Fast 3G** or **Slow 3G**.
5.  Start training by clicking the "Play" button in the UI.
6.  **Observation**:
    - The training loss graph should continue to update reasonably smoothly.
    - The background visualization (classification map) might update less frequently (framerate drops), but the interaction should remain responsive.
    - The "Steps/Sec" counter should remain high (close to non-throttled performance), indicating the backend training is not blocked by the network.

## Troubleshooting

- If the UI freezes: The main thread might still be blocked. Check server logs.
- If "Steps/Sec" drops drastically: The decoupling might not be working, or the queue is filling up and blocking the producer.
