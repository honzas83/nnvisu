# Research: Dense Probabilistic Grid

## 1. Grid Resolution Strategy

**Goal**: Increase grid density by 2x in each direction.

-   **Current**: 50x50 points (2,500 total).
-   **Target**: 100x100 points (10,000 total).

**Implications**:
-   **Inference**: A 4x increase in inference batch size. For a simple neural network (e.g., [2, 10, 5, 3]), this is negligible on modern CPUs/GPUs (milliseconds).
-   **Bandwidth**: 
    -   If sending Class IDs (1 byte/pixel): 2.5KB -> 10KB.
    -   If sending RGB (3 bytes/pixel): 7.5KB -> 30KB.
    -   Both are well within WebSocket capacity for realtime usage (typical limits are MBs).

**Decision**: Update `generate_map` to use `width=100, height=100`.

## 2. Probabilistic Color Blending Strategy

**Goal**: Color the grid based on posterior probabilities.

**Alternatives Considered**:

1.  **Frontend Blending (Send Probabilities)**
    -   Send raw probabilities (e.g., 3 floats per pixel) to the client.
    -   Client performs interpolation in JS/Shader.
    -   *Pros*: Client allows dynamic color changes without re-inference.
    -   *Cons*: Large payload (100x100x3 floats = ~120KB/frame). Higher JS processing load.
    
2.  **Backend Blending (Send Pre-rendered Colors)**
    -   Calculate `Softmax` on backend.
    -   Perform weighted average of class colors: $C_{final} = \sum P_i \times C_i$.
    -   Send final RGB(A) bytes.
    -   *Pros*: Small payload (~30KB for RGB). Fast implementation in NumPy/PyTorch.
    -   *Cons*: Colors are fixed on backend (must match frontend point colors).

**Decision**: **Backend Blending**.
-   **Rationale**: It minimizes network traffic and offloads computation to the more efficient NumPy/PyTorch environment. It simplifies the frontend rendering logic (just blit the image data).
-   **Implementation**:
    -   Define Class Colors in `trainer.py` to match `main.js` (Blue: #3498db, Orange: #e67e22, Red: #e74c3c).
    -   Use `torch.softmax(outputs, dim=1)` to get probabilities.
    -   Compute weighted sum of RGB vectors.
    -   Output raw RGB bytes.

## 3. Data Transmission

-   **Format**: Base64 encoded binary string.
-   **Schema**:
    -   `type`: "map_update"
    -   `payload`:
        -   `width`: 100
        -   `height`: 100
        -   `format`: "rgb" (New field to indicate data format change)
        -   `data`: Base64 string

## 4. Performance Impact

-   **Latency**: 100x100 inference + color blending + B64 encoding should easily stay under 50ms on standard hardware.
-   **Memory**: Negligible increase.

## 5. Security

-   No new inputs introduced.
-   Standard WebSocket validation applies.
