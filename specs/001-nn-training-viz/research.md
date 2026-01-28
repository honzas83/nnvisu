# Research Findings: Visualise Neural Network Training

**Branch**: `001-nn-training-viz`

## Decisions

### 1. Neural Network Library: PyTorch
**Decision**: Use **PyTorch** (CPU-only build for simplicity) for the neural network backend.
**Rationale**:
- **Granular Control**: We need to step through training (epoch by epoch or batch by batch) to stream updates. PyTorch's `optimizer.step()` loop is explicit and easy to instrument.
- **Extensibility**: If we want to visualize gradients or change architectures later, PyTorch makes this trivial compared to Scikit-learn.
- **Standard**: It is the de-facto standard for deep learning; familiar to most developers.
**Alternatives Considered**:
- *Scikit-Learn (`MLPClassifier`)*: Supports `partial_fit`, but is less flexible for custom architectural changes or detailed introspection (e.g., gradients).
- *Pure NumPy*: Good for education, but maintaining backprop code for different architectures is error-prone and reinvents the wheel.

### 2. Visualization Data Transport: Base64 Encoded Bitmap
**Decision**: Stream the classification map as a **Base64-encoded PNG or Raw Bytes** embedded in the JSON Websocket message.
**Rationale**:
- **Simplicity**: Keeps the Websocket protocol purely text-based (JSON).
- **Performance**: A 100x100 visualization grid (sufficient for a background heatmap) is 10,000 pixels.
    - Raw: 10KB.
    - Base64: ~13.5KB.
    - At 20 FPS, this is ~270KB/s, which is negligible for localhost/LAN.
- **Handling**: JS `Image` object can easily load `data:image/png;base64,...` or we can parse raw bytes into a `Canvas` `ImageData` array.
**Refinement**: We will send **Raw Class IDs** (flattened array) encoded as Base64.
    - The frontend maps Class IDs to colors. This decouples the backend from styling.
    - 100x100 grid of classes (0-255) = 10KB payload.

### 3. Frontend Architecture: Vanilla JS + Canvas API
**Decision**: Use **Vanilla JavaScript** with the **HTML5 Canvas API**.
**Rationale**:
- **Performance**: Canvas is designed for pixel manipulation (perfect for the classification map) and drawing many points.
- **Overhead**: React/Vue are overkill for a single-page interactive demo. Direct DOM/Canvas manipulation is most performant and simplest for this specific use case.
- **State**: State is simple (Training vs Idle, List of Points). Global JS object or simple module is sufficient.

## Open Questions Resolved

- **Unknown**: Efficient serialization? -> **Base64 Class ID Grid**.
- **Unknown**: Library? -> **PyTorch**.
