# Research: Dynamic Architecture & 3rd Class

**Status**: Complete
**Date**: 2026-01-28

## Decisions

### 1. Neural Network Architecture Configuration
*   **Decision**: Update `NeuralNetwork` class to accept `output_dim` and a dynamic `hidden_layers` list. The `nn.Sequential` block will be constructed by iterating over `hidden_layers`.
*   **Rationale**: This allows complete flexibility for the user while keeping the implementation simple using standard PyTorch modules.
*   **Alternatives Considered**:
    *   *Hardcoded complexity tiers (e.g., Simple, Medium, Complex)*: Rejected because the user wants specific control (e.g., "10-5").
    *   *Graph-based definition*: Rejected as too complex for this phase.

### 2. Multi-Class Visualization
*   **Decision**: Update the frontend canvas rendering to handle 3 classes.
    *   **Class 0**: Blue (`#3498db`) - Existing
    *   **Class 1**: Orange (`#e67e22`) - Existing
    *   **Class 2**: Red (`#e74c3c`) - New
*   **Rationale**: Distinct colors that are colorblind-friendly enough for this prototype (though accessible palettes should be considered in future). Matches the "Red" requirement explicitly.

### 3. Architecture Input Handling
*   **Decision**: Use a simple text input with hyphen delimiters (e.g., "10-5"). Validation will run on the client side (regex) before sending, and server-side (pydantic/logic) before applying.
*   **Rationale**: Fastest way for users to type. A visual builder is overkill.
*   **Soft Limits**: Max 10 layers, 100 neurons per layer. Enforced on Server.

### 4. Websocket Protocol Updates
*   **Decision**: Add a payload to the `RESET_MODEL` message type.
    *   Old: `{"type": "RESET_MODEL"}`
    *   New: `{"type": "RESET_MODEL", "payload": {"hidden_layers": [10, 5]}}`
*   **Rationale**: Re-uses the existing reset channel but adds necessary configuration data.

## Unknowns Resolved

*   **Handling >2 Classes in PyTorch**: Confirmed that `CrossEntropyLoss` handles multi-class classification natively if passed raw logits of shape `(N, C)` and targets of shape `(N)`. The model currently outputs logits, so this fits perfectly.
*   **Frontend Rendering**: The `MAP_UPDATE` message sends a byte array of class IDs. We just need to add a condition `if (cls === 2)` to set the red pixel color.
