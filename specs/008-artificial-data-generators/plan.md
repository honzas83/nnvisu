# Implementation Plan: Artificial Data Generators

**Branch**: `008-artificial-data-generators` | **Date**: 2026-02-03 | **Spec**: [specs/008-artificial-data-generators/spec.md](spec.md)
**Input**: Feature specification from `/specs/008-artificial-data-generators/spec.md`

## Summary

The goal is to implement a row of buttons in the "Training data" section that allows users to generate classic artificial datasets (Circles, Moons, Blobs, Anisotropic, Varied Variance) with configurable class counts. The data generation will likely happen on the backend using NumPy to ensure consistency with the training loop, then synchronized via WebSockets to the frontend for visualization.

## Technical Context

**Language/Version**: Python 3.11+, JavaScript (ES6)  
**Primary Dependencies**: Tornado (WebSockets), NumPy (Mathematical distributions), PyTorch (Backend model), Browser Canvas API (Frontend rendering)  
**Storage**: N/A (In-memory training state)  
**Testing**: `pytest` for backend logic, Manual/Integration for frontend synchronization  
**Target Platform**: Web (Chrome/Firefox/Safari)
**Project Type**: Full-stack Web (Tornado Backend + Vanilla JS Frontend)  
**Performance Goals**: <300ms from button click to canvas render  
**Constraints**: <50ms processing time for WebSocket messages on backend  
**Scale/Scope**: 5 distribution types, up to 6 classes, 200 points per dataset

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Strict Typing**: Use type hints for all new Python functions in `trainer.py` or new `generators.py`.
- [x] **Realtime-First**: NumPy generation should be fast; ensure it doesn't block the Tornado event loop for excessive periods.
- [x] **Rigorous Testing**: Add unit tests for each distribution generator.
- [x] **UX Consistency**: New UI row must match the styling of existing "Training data" controls.

## Project Structure

### Documentation (this feature)

```text
specs/008-artificial-data-generators/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/nnvisu/
├── app.py               # Tornado App
├── handlers.py          # WebSocket Handlers
├── protocol.py          # Message definitions
├── logic/
│   ├── trainer.py       # Needs update for dataset replacement
│   └── generators.py    # NEW: NumPy-based dataset generators
└── static/
    ├── index.html       # Add UI row
    ├── main.js          # Handle button clicks
    ├── state_manager.js # Update training state
    └── style.css        # Styling for new buttons
```

**Structure Decision**: Single project structure (Option 1). We are extending the existing `src/nnvisu` package.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations identified.*