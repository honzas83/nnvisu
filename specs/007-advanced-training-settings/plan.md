# Implementation Plan: Advanced Training Settings

**Branch**: `007-advanced-training-settings` | **Date**: 2026-02-02 | **Spec**: [spec.md](./spec.md)

## Summary

This feature adds an "Advanced Options" panel to the UI, allowing users to tune technical hyperparameters including activation functions (tanh, ReLU, Leaky ReLU, GELU), optimizers (SGD, ADAM, RMSProp), learning rate, L2 weight regularization, batch size, and dropout. The backend is updated to support dynamic model reconstruction and optimizer selection based on these parameters.

## Technical Context

**Language/Version**: Python 3.11+, JavaScript (ES6)
**Primary Dependencies**: Tornado (WebSockets), PyTorch (NN Core), NumPy
**Storage**: N/A (In-memory), LocalStorage for frontend settings
**Testing**: pytest (Backend logic), Manual (Frontend UI)
**Target Platform**: Modern Web Browsers
**Project Type**: Web Application (Single Repo)
**Performance Goals**: <50ms per training step update
**Constraints**: Keep UI clean; Advanced panel should not distract beginners.

## Constitution Check

- [x] **High Assurance Code Quality**: Strictly type Python signatures for new activation/optimizer factories.
- [x] **Realtime-First Architecture**: Realtime updates from JS inputs ensure immediate visual feedback.
- [x] **Rigorous Testing Standards**: Unit tests will verify the `NeuralNetwork` module switching logic.
- [x] **User Experience Consistency**: Collapsible box preserves simple UX while offering power features.

## Project Structure

### Documentation (this feature)

```text
specs/007-advanced-training-settings/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── websocket.md
```

### Source Code

```text
src/nnvisu/
├── logic/
│   ├── model.py         # UPDATED: Support multiple activations and dropout
│   └── trainer.py       # UPDATED: Support multiple optimizers and mini-batching
├── static/
│   ├── index.html       # UPDATED: Add Advanced box below canvas
│   ├── style.css        # UPDATED: Styling for Advanced panel and tooltips
│   └── main.js          # UPDATED: Bind new inputs to StateManager and WS
└── handlers.py          # UPDATED: Pass advanced config to Trainer
```

**Structure Decision**: Single project (Option 1).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |