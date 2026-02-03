# Feature Specification: Responsive Layout

**Feature Branch**: `009-responsive-layout`
**Created**: 2026-02-03
**Status**: Draft
**Input**: User description: "Add responsivity. If the screen is wide enough, place canvas to the right and keep toolboxes on the left."

## Clarifications

### Session 2026-02-03
- Q: How should scrolling behave in the wide layout? → A: Left column (controls) scrolls independently; Right column (canvas) is sticky/fixed.
- Q: How should column widths be distributed in the wide layout? → A: Fixed width left (controls), flexible right (canvas).
- Q: What should be the stack order in the narrow layout? → A: Controls/toolboxes on top, canvas below (as is currently).
- Q: How should the canvas resize in the narrow layout? → A: Canvas shrinks to fit screen width (maintains aspect ratio).
- Q: Where should the "How-to" section be placed in the wide layout? → A: Keep it at the top of the left (controls) column.
- Q: Should project metadata, CPU-only PyTorch, and WebSocket fixes be included? → A: Yes, include project metadata, CPU-only PyTorch, and WebSocket proxy fixes in this spec.
- Q: How should the WebSocket proxy URL be resolved? → A: Automatically match page protocol (ws if http, wss if https).
- Q: Where should metadata be implemented and how should PyTorch be handled? → A: Update `pyproject.toml` and `src/nnvisu/__init__.py`; add dependency on pytorch CPU-only.
- Q: How should proxy support be verified? → A: Functional verification at subpath behind proxy.

## User Scenarios & Testing *(mandatory)*
...
### Functional Requirements

- **FR-001**: The system MUST detect the viewport width and apply different layouts based on a breakpoint.
...
- **FR-012**: The "Advanced Options" panel MUST be grouped with the other toolboxes/controls on the left side in the wide layout.
- **FR-013**: Project metadata MUST be updated: Author: Jan Švec <honzas@kky.zcu.cz>, Version: 1.0.
- **FR-014**: The backend training logic MUST be forced to use CPU only for PyTorch operations.
- **FR-015**: The frontend WebSocket connection MUST automatically detect the protocol (ws/wss) based on the current page protocol to support hosting behind proxies.
- **FR-016**: The WebSocket connection MUST use a relative path or correct proxy-aware URL resolution to prevent connection failures when hosted on subpaths.
- **FR-017**: The project configuration (`pyproject.toml`) MUST specify the CPU-only version of PyTorch to ensure compatibility in restricted environments.
- **FR-018**: The application MUST retrieve its version and author information from the centralized Python metadata (e.g., `src/nnvisu/__init__.py`).

### Key Entities

- **Project Metadata**:
    - **Author**: Jan Švec <honzas@kky.zcu.cz> (sourced from department info)
    - **Version**: 1.0
    - **Environment**: Forced CPU-only training.

### Assumptions

- The specific breakpoint value (e.g., 1024px or 1200px) can be tuned during implementation but must provide a reasonable desktop experience.
- "Toolboxes" includes the main header controls and the advanced settings panel.
- The footer can remain at the bottom of the entire page or bottom of the left column, as appropriate for the design.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Layout automatically switches between single-column and two-column modes instantly (under 100ms visual latency) upon resizing past the breakpoint.
- **SC-002**: In wide mode, the canvas and controls are simultaneously visible without scrolling on a standard 1080p screen.
- **SC-003**: No horizontal scrollbar appears on the page body in either layout mode (content fits viewport width).
- **SC-004**: The application is fully functional (training starts, updates received) when accessed through a reverse proxy at a subpath (e.g., `/nnvisu/`).