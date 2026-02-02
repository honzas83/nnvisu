# Research: GUI Dynamic Classes

## 1. Dynamic Class Weight Adaptation

**Goal**: Incremental adaptation of the model's output layer when class count changes.

**Decision**:
-   Implement `StatelessTrainer.adapt_model_to_classes(model, new_num_classes)` on the backend.
-   When `new_num_classes > current_num_classes`: Append new randomly initialized rows (for weights) and zeros (for biases) to the output layer.
-   When `new_num_classes < current_num_classes`: Slice the weight matrix and bias vector to the new size.
-   **Note**: This assumes classes are always contiguous starting from 0. If class 1 is removed but 0 and 2 remain, the backend needs to map them to [0, 1] internally or the frontend must normalize.

## 2. Training History and Seekbar

**Goal**: Store up to 256 snapshots of the decision map, pruning every 2nd if full.

**Decision**:
-   **Storage**: Client-side (JS) is better to avoid massive server memory usage. Each 100x100 RGB snapshot is ~30KB. 256 snapshots = ~7.5MB. Perfectly fine for `localStorage` (if within limits) or better, in-memory `Array`.
-   **Pruning**:
    ```javascript
    if (history.length >= 256) {
        history = history.filter((_, i) => i % 2 === 0);
        recordingInterval *= 2;
    }
    ```
-   **Subsampling**: Start with an interval of `N=10` epochs/steps.

## 3. Tool Logic (Draw vs Eraser)

**Goal**: Mutually exclusive modes, large circular cursor for eraser.

**Decision**:
-   State variable `currentTool` ('draw' | 'erase').
-   `currentTool` is set to 'draw' when a color is picked.
-   `currentTool` is set to 'erase' when eraser button is clicked.
-   Eraser radius: ~20px (on 800x800 canvas).
-   Visual Feedback: `viz-canvas` will render a "ghost" circle at mouse coordinates when eraser is active.

## 4. UI Layout Changes

-   **Palette**: Row of 8-10 color circles/squares.
-   **Play/Pause**: Toggle button with dynamic text/icon.
- **Seekbar**: `<input type="range">` that updates when training pauses or when user scrubs.
- **Header**: Update title to "nnvisu" and add a concise "How to use" section (e.g., "1. Click to add points, 2. Press Play to train, 3. Scrub history to review").
- **Branding**: Footer update in `index.html` with author details and GitHub link.
- **Instant Redraw**: Reset button immediately sends a `map_update` request or triggers a local clear.

## 5. Technical Constraints

-   **WebSocket**: Needs a new message type for "reset" or "redraw" if the server maintains state, but since it's `StatelessTrainer`, the client just sends the current (possibly new/reset) weights and gets a map back.
-   **Model Re-init**: `NeuralWebSocket` currently reconstructs the model every step. It needs to handle the `output_dim` dynamically based on the max label in `data_points`.
