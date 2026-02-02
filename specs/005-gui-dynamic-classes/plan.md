# Implementation Plan: GUI Dynamic Classes

**Branch**: `005-gui-dynamic-classes` | **Date**: 2026-02-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/005-gui-dynamic-classes/spec.md`

## Summary

This feature significantly upgrades the user interface and core training logic of `nnvisu`. Key enhancements include a dynamic number of classes via a color palette, an eraser tool for data management, a unified Play/Pause control, and a training history seekbar. The backend is updated to incrementally adapt the model's output layer weights when classes are added or removed, preserving training progress.

## Technical Context

**Language/Version**: Python 3.11+, JavaScript (ES6)
**Primary Dependencies**: Tornado (Backend), PyTorch (Inference/Training), Browser Canvas API (Frontend)
**Storage**: `localStorage` (Configuration/Data), In-memory (Training History)
**Testing**: pytest (Backend), Manual Browser Verification (Frontend)
**Target Platform**: Web Browser
**Project Type**: Web Application
**Performance Goals**: <50ms for eraser interactions, <200ms for weight reset redraw.
**Constraints**: 256 snapshot limit for history to prevent memory bloat.

## Constitution Check

- [x] **High Assurance Code Quality**: All Python changes will be strictly typed and linted.
- [x] **Realtime-First Architecture**: GUI updates and tool interactions remain responsive and unblocked.
- [x] **Rigorous Testing Standards**: Backend weight adaptation logic will be covered by unit tests.
- [x] **User Experience Consistency**: New controls (Play/Pause, Seekbar) follow standard UX patterns.

## Project Structure

### Documentation (this feature)

```text
specs/005-gui-dynamic-classes/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── websocket.md
└── tasks.md
```

### Source Code

```text
src/nnvisu/
├── logic/
│   ├── trainer.py       # UPDATED: Weight adaptation logic
│   └── model.py         # UPDATED: Incremental layer resizing
├── static/
│   ├── index.html       # UPDATED: Header (Title, How-to), Palette, Seekbar, Footer
│   ├── main.js          # UPDATED: Tool modes, Play/Pause, History management
│   └── style.css        # UPDATED: Palette and UI styling
└── handlers.py          # UPDATED: Handle dynamic class counts in payload
```

**Structure Decision**: Single project (Option 1).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Incremental weight adaptation | Preserve training progress when adding classes | Rebuilding from scratch is jarring and loses progress |