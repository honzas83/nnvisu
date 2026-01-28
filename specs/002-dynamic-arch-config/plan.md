# Implementation Plan: Dynamic Architecture & 3rd Class

**Branch**: `002-dynamic-arch-config` | **Date**: 2026-01-28 | **Spec**: [specs/002-dynamic-arch-config/spec.md](../spec.md)
**Input**: Feature specification from `/specs/002-dynamic-arch-config/spec.md`

## Summary

This feature enables users to dynamically configure the neural network's hidden layer architecture (e.g., "10-5") via a frontend input box. It also introduces a 3rd target class (Red) for data generation and visualization, expanding the problem space from binary to multi-class classification. The system will enforce soft limits on complexity (max 10 layers, 100 neurons/layer) and automatically handle input/output layer sizing based on the 2D input and 3 target classes.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**:
-   **Backend**: Tornado (Websockets), PyTorch (Neural Network), NumPy (Data processing)
-   **Frontend**: Vanilla JS, HTML/CSS
**Storage**: N/A (In-memory training state)
**Testing**: pytest (Backend), manual/integration (Frontend)
**Target Platform**: Local development (macOS/Linux/Windows)
**Project Type**: Web application (Backend + Frontend)
**Performance Goals**: Real-time architecture updates (<5s), smooth visualization (60fps), training updates via Websocket (<50ms latency)
**Constraints**:
-   Soft limit: max 10 hidden layers, max 100 neurons/layer.
-   Input fixed to 2D.
-   Output dynamic based on class count (currently 2, extending to 3).
**Scale/Scope**: Small feature addition, touches logic (model.py), handlers, and frontend.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   **High Assurance Code Quality**:
    *   **Pass**: Will maintain strict typing (mypy) and linting (ruff).
    *   **Action**: Ensure `NeuralNetwork` class updates are fully typed.
*   **Realtime-First Architecture**:
    *   **Pass**: Uses existing Websocket architecture for updates.
    *   **Action**: Ensure architecture update triggers a clean reset without blocking the event loop.
*   **Rigorous Testing Standards**:
    *   **Pass**: Logic changes in `model.py` and `trainer.py` will be unit tested.
    *   **Action**: Add unit tests for `NeuralNetwork` with various configurations and invalid inputs.
*   **User Experience Consistency**:
    *   **Pass**: New input and class button will match existing UI style.
    *   **Action**: Immediate feedback on "Enter" or blur matches expectation.
*   **Performance & Limits**:
    *   **Pass**: Soft limits (10 layers, 100 neurons) explicitly added to prevent degradation.

## Project Structure

### Documentation (this feature)

```text
specs/002-dynamic-arch-config/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── logic/
│   │   ├── model.py     # Update NeuralNetwork to accept output_dim and dynamic hidden layers
│   │   └── trainer.py   # Update to handle 3 classes (data generation)
│   ├── handlers.py      # Update WS handler if schema changes
│   └── app.py
└── tests/
    └── unit/            # Add tests for dynamic architecture

frontend/
├── src/
│   ├── index.html       # Add architecture input and Class 2 button
│   ├── main.js          # Handle input events and 3rd class logic
│   └── style.css        # Style for new controls
└── tests/
```

**Structure Decision**: Standard Web Application structure (Backend + Frontend) as detected.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |
