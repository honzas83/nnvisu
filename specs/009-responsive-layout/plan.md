# Implementation Plan: Responsive Layout

**Branch**: `009-responsive-layout` | **Date**: 2026-02-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/009-responsive-layout/spec.md`

## Summary

The goal is to implement a responsive layout for the `nnvisu` application. On wide screens (>1024px), the layout will feature a two-column design with a fixed-width controls column on the left and a flexible-width visualization canvas on the right. The left column will scroll independently, while the canvas remains sticky. On narrow screens (<1024px), the layout will stack vertically with controls on top. Additionally, the plan includes updating project metadata (Author: Jan Švec, Version: 1.0), forcing PyTorch to CPU-only mode, and fixing WebSocket connectivity for proxied environments (e.g., https://dialogs.kky.zcu.cz/nnvisu/).

## Technical Context

**Language/Version**: Python 3.11+, JavaScript (ES6)
**Primary Dependencies**: Tornado, PyTorch (CPU-only), NumPy, Browser Canvas API
**Storage**: `localStorage` (Configuration/Data), In-memory (Training History)
**Testing**: `pytest`
**Target Platform**: Modern Browsers, Python 3.11+ Backend
**Project Type**: Web application (Frontend + Backend)
**Performance Goals**: Layout switching <100ms, persistent 60fps for canvas updates.
**Constraints**: Must work behind a reverse proxy on a subpath. PyTorch must be CPU-only.
**Scale/Scope**: Single-page application, in-memory training state.

## Constitution Check

*GATE: Passed on 2026-02-03.*

- **Principle I (Code Quality)**: [PASSED] All Python changes will be strictly typed and pass `ruff` and `mypy`.
- **Principle II (Realtime Architecture)**: [PASSED] WebSocket URL resolution is enhanced to be proxy-aware while remaining non-blocking.
- **Principle III (Testing)**: [PASSED] Manual verification steps for layout and proxy support are defined in quickstart.md.
- **Principle IV (UX Consistency)**: [PASSED] Responsive layout ensures consistent experience across devices.

## Project Structure

### Documentation (this feature)

```text
specs/009-responsive-layout/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/
└── nnvisu/
    ├── __init__.py      # Version and Author metadata
    ├── __main__.py
    ├── app.py           # Backend startup (CPU-only force)
    ├── handlers.py
    ├── protocol.py
    ├── logic/
    │   ├── generators.py
    │   ├── model.py     # PyTorch model (CPU device force)
    │   └── trainer.py
    └── static/
        ├── index.html   # Layout structure updates
        ├── main.js      # WebSocket proxy fix
        ├── state_manager.js
        └── style.css    # Flexbox/Grid responsive layout
```

**Structure Decision**: Single project structure as defined in the existing codebase. The `nnvisu` package contains both backend and frontend static assets.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |