# Implementation Plan: Usability Layout Refactor

**Branch**: `006-usability-layout-refactor` | **Date**: 2026-02-02 | **Spec**: [spec.md](./spec.md)

## Summary

This feature refactors the UI of `nnvisu` to improve usability and logical organization. Controls are grouped into two panels: "Training Data" and "Training & History". The "Arch" input is renamed to be more descriptive, a "How to use" guide is added, and training status metrics are integrated with the history seekbar for better contextual visibility. Additionally, the system is optimized to instantly redraw the visualization when model weights are reset.

## Technical Context

**Language/Version**: Python 3.11+, JavaScript (ES6)
**Primary Dependencies**: Tornado, PyTorch, Browser Canvas API
**Storage**: N/A (UI Refactor)
**Testing**: Manual Browser Verification
**Target Platform**: Web Browser
**Project Type**: Web Application
**Performance Goals**: N/A
**Constraints**: Keep layout responsive and visually balanced.

## Constitution Check

- [x] **High Assurance Code Quality**: Strict CSS/HTML standards.
- [x] **Realtime-First Architecture**: Ensure UI updates remain snappy during training.
- [x] **Rigorous Testing Standards**: Visual verification of all user stories.
- [x] **User Experience Consistency**: Grouping and descriptive labels enhance consistency.

## Project Structure

### Documentation (this feature)

```text
specs/006-usability-layout-refactor/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── tasks.md
```

### Source Code

```text
src/nnvisu/static/
├── index.html       # UPDATED: Grouped sections, new header, integrated status
├── style.css        # UPDATED: Panel styling, constrained seekbar width
└── main.js          # UPDATED: DOM element ID updates if necessary
```

**Structure Decision**: Single project (Option 1).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |