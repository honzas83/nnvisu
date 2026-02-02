# Tasks: Usability Layout Refactor

**Feature Branch**: `006-usability-layout-refactor`
**Plan File**: `specs/006-usability-layout-refactor/plan.md`
**Status**: Done

## Implementation Strategy

This feature focuses on UI/UX improvements. We will begin by establishing the new layout structure in CSS and HTML, followed by descriptive labeling and onboarding content. Finally, we will implement the functional integration of training metrics with the history seekbar and optimize the model reset behavior for instant visual feedback.

## Dependencies

1.  **Phase 2 & 3** establish the layout container structure which is a prerequisite for moving elements in **Phase 6**.
2.  **Phase 7** is a standalone functional optimization but should be tested alongside the UI changes.

---

## Phase 1: Setup
**Goal**: Verify current visual state and prepare for refactor.

- [x] T001 Review `src/nnvisu/static/style.css` and identify existing layout constraints to ensure a clean transition.

## Phase 2: Foundational
**Goal**: Establish the CSS framework for grouped control panels.

- [x] T002 Add CSS rules for `.control-panel` containers and headers in `src/nnvisu/static/style.css` to support logical grouping.

## Phase 3: User Story 1 - Organized Control Interface (P1)
**Goal**: Group controls into "Training Data" and "Training & History" sections.

- [x] T003 [US1] Wrap Palette, Eraser, and Clear Data buttons in a "Training Data" panel in `src/nnvisu/static/index.html`.
- [x] T004 [US1] Wrap Play/Pause, Architecture, Reset, and History Seekbar in a "Training & History" panel in `src/nnvisu/static/index.html`.

## Phase 4: User Story 2 - Descriptive Model Configuration (P1)
**Goal**: Improve clarity of the architecture input.

- [x] T005 [US2] Update the "Arch:" label to "Network Architecture (Hidden Layers)" and add an example (e.g., "10-5-2") in `src/nnvisu/static/index.html`.

## Phase 5: User Story 3 - Instant Onboarding (P2)
**Goal**: Add a concise usage guide for new users.

- [x] T006 [US3] Implement a 4-step "How to use" ordered list below the main header in `src/nnvisu/static/index.html`.

## Phase 6: User Story 4 - Compact History & Status Integration (P2)
**Goal**: Constrain seekbar width and move metrics for better context.

- [x] T007 [US4] Constrain the maximum width of the history seekbar to match the canvas (e.g., 800px) in `src/nnvisu/static/style.css`.
- [x] T008 [US4] Relocate the `#status` and `#metrics` display elements from the footer to the "Training & History" panel in `src/nnvisu/static/index.html`.
- [x] T009 [US4] Verify and update metrics display styling in `src/nnvisu/static/style.css` to ensure they fit correctly within the panel.

## Phase 7: Functional Optimization
**Goal**: Ensure instant visual feedback on model reset.

- [x] T010 [P] Update `resetModel()` in `src/nnvisu/static/main.js` to trigger an immediate `runTrainingLoop()` call to redraw the map with new weights.

## Phase 8: Polish & Cross-Cutting Concerns
**Goal**: Finalize layout and verify all user stories.

- [x] T011 [P] Ensure layout responsiveness (vertical stacking) for narrow viewports in `src/nnvisu/static/style.css`.
- [x] T012 Conduct manual end-to-end verification of all acceptance scenarios in the browser.