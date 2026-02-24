# Implementation Plan - Fix architecture synchronization between UI and network

**Branch**: `011-fix-arch-sync` | **Date**: 2026-02-24 | **Spec**: [specs/011-fix-arch-sync/spec.md](spec.md)
**Input**: Feature specification from `/specs/011-fix-arch-sync/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

This feature addresses the synchronization gap between the UI's architectural representation (layers/neurons) and the backend's neural network model. Currently, changes in the UI may not be reflected in the actual network being trained. This plan ensures immediate synchronization, re-initialization of weights on structure changes, and strict validation of architectural constraints.

## Technical Context

**Tech Stack**: Python 3.11+, Tornado (WebSockets), PyTorch (NN Core), NumPy, JavaScript (ES6), Browser Canvas API  
**Existing Components**: 
- `src/nnvisu/logic/model.py`: Likely contains the PyTorch model definition.
- `src/nnvisu/logic/trainer.py`: Manages the training loop.
- `src/nnvisu/protocol.py`: Defines the WebSocket message protocol.
- `src/nnvisu/static/main.js`: Handles UI interactions and WebSocket communication.
**Infrastructure**: N/A (In-memory training state)  
**Dependencies**: `torch`, `tornado`, `numpy`  
**Storage**: `localStorage` (Configuration/Data), In-memory (Training History)  
**Testing**: `pytest` for backend, manual/integration tests for UI-backend sync.  
**Target Platform**: Modern Web Browsers, Python 3.11+ Backend.
**Project Type**: web-service  
**Performance Goals**: Architecture sync < 100ms.  
**Constraints**: Max 10 hidden layers, 100 neurons per layer.  
**Scale/Scope**: Single-user realtime training visualization.

### Unknowns & Research Needed (NEEDS CLARIFICATION)

1. **Model Re-initialization Strategy**: How does the current `model.py` handle structural changes? Does it require a full object recreation or can it dynamically adjust layers? (NEEDS CLARIFICATION)
2. **WebSocket Message Type**: Is there an existing message type for "update architecture" in `protocol.py`? (NEEDS CLARIFICATION)
3. **State Consistency during Training**: What is the current mechanism to pause/stop training safely in `trainer.py`? (NEEDS CLARIFICATION)

## Constitution Check

### I. High Assurance Code Quality
- **Plan**: Ensure all new backend logic in `model.py` and `handlers.py` is fully type-hinted.
- **Validation**: Run `ruff check` and `mypy` on `src/nnvisu/`.

### II. Realtime-First Architecture
- **Plan**: Use asynchronous WebSocket handlers for architecture updates to avoid blocking the Tornado event loop.
- **Validation**: Ensure no `time.sleep` or blocking PyTorch calls in the main thread.

### III. Rigorous Testing Standards
- **Plan**: Add unit tests for `model.py` to verify layer resizing and weight re-initialization. Add integration tests for the WebSocket "update architecture" flow.
- **Validation**: `pytest tests/unit/test_model_dynamic.py` and new integration tests.

### IV. User Experience Consistency
- **Plan**: Immediate UI feedback when changing layers; ensure the visual network diagram matches the backend state.
- **Validation**: Manual verification of UI-backend parity.

## Gate Evaluation

| Gate | Status | Justification |
|------|--------|---------------|
| **Security** | PASS | No sensitive data or auth involved in this sync fix. |
| **Performance** | PASS | Sync < 100ms is feasible for small model re-creations. |
| **Compliance** | PASS | Aligns with project constraints (10 layers/100 neurons). |
| **Stability** | PASS | Auto-stop/reset on architecture change prevents shape mismatch crashes. |

## Phase 0: Outline & Research

### Research Tasks

1. **Research Model Dynamic Reconfiguration**: Investigate `src/nnvisu/logic/model.py` to see how it currently builds the network and if it supports dynamic updates.
2. **Research WebSocket Protocol**: Audit `src/nnvisu/protocol.py` for architecture-related message definitions.
3. **Research Trainer Lifecycle**: Examine `src/nnvisu/logic/trainer.py` to understand the training loop's pause/stop/restart logic.

## Phase 1: Design & Contracts

### Artifacts to Generate
- `research.md`: Consolidate findings from Phase 0.
- `data-model.md`: Define the `NetworkConfiguration` and `NeuralModel` state.
- `contracts/websocket.md`: Define the architecture update message schema.
- `quickstart.md`: Define the test scenario for verifying sync.

## Phase 2: Implementation Strategy

1. **Backend - Model**: Update `model.py` to support full re-initialization from a new configuration object.
2. **Backend - Protocol**: Define `MSG_TYPE_UPDATE_ARCH` message.
3. **Backend - Handlers**: Update WebSocket handlers to process architecture changes and signal the `Trainer`.
4. **Backend - Trainer**: Implement safe "stop and reset" logic when architecture changes.
5. **Frontend - State**: Update `state_manager.js` and `main.js` to send sync messages immediately on UI interaction.
6. **Frontend - UI**: Implement validation (max layers/neurons) and visual feedback for the sync state.
