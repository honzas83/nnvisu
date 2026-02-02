# Tasks: GUI Dynamic Classes

**Feature Branch**: `005-gui-dynamic-classes`
**Plan File**: `specs/005-gui-dynamic-classes/plan.md`
**Status**: Done

## Implementation Strategy

We will follow a prioritized approach, starting with the core functional changes to the model architecture and data management (Dynamic Classes and Eraser), followed by UX improvements (Play/Pause, Reset behavior), and finally adding the analytical and branding features (History Seekbar, Footer). 

The backend changes for incremental weight adaptation are foundational and will be implemented and tested first to ensure stability as the UI evolves to support dynamic classes.

## Dependencies

1. **Phase 2 (Foundational)** must be completed before **Phase 3 (US1)** to support dynamic class counts.
2. **Phase 3 (US1)** and **Phase 4 (US2)** can be developed in parallel as they touch different parts of the frontend state.
3. **Phase 6 (US4)** depends on the Play/Pause logic in **Phase 5 (US3)** for better control of the historical state.

---

## Phase 1: Setup
**Goal**: Initialize test environment for backend logic.

- [x] T001 Create backend unit tests for weight adaptation logic in `tests/unit/test_model_adaptation.py`

## Phase 2: Foundational
**Goal**: Implement incremental model resizing on the backend.

- [x] T002 Implement `adapt_output_layer` method in `NeuralNetwork` class in `src/nnvisu/logic/model.py`
- [x] T003 Update `StatelessTrainer.train_step` to handle dynamic output dimensions in `src/nnvisu/logic/trainer.py`
- [x] T004 Update `NeuralWebSocket.handle_train_step` to detect required `output_dim` from payload data in `src/nnvisu/handlers.py`

## Phase 3: User Story 1 - Dynamic Class Management (P1)
**Goal**: Enable arbitrary class count via color palette.
**Independent Test**: User can add points of 5 different colors and the model trains with 5 output classes.

- [x] T005 [P] [US1] Create color palette UI component (8-10 colors) in `src/nnvisu/static/index.html`
- [x] T006 [P] [US1] Add palette styling (circles/squares) in `src/nnvisu/static/style.css`
- [x] T007 [US1] Implement palette selection logic and tool mode toggle in `src/nnvisu/static/main.js`
- [x] T008 [US1] Ensure `runTrainingLoop` sends correct class count to server in `src/nnvisu/static/main.js`

## Phase 4: User Story 2 - Data Point Eraser (P1)
**Goal**: Enable targeted data deletion with visual feedback.
**Independent Test**: Selecting Eraser and clicking a point removes it from the canvas and the trained model.

- [x] T009 [P] [US2] Add Eraser button to UI in `src/nnvisu/static/index.html`
- [x] T010 [US2] Implement radius-based point deletion logic in `src/nnvisu/static/main.js`
- [x] T011 [US2] Implement circular cursor preview for Eraser tool on canvas in `src/nnvisu/static/main.js`

## Phase 5: User Story 3 - Training Flow Control (P2)
**Goal**: Unified Play/Pause and responsive Reset.
**Independent Test**: Button toggles between Play/Pause; Reset clears the decision map instantly.

- [x] T012 [P] [US3] Replace Start/Stop buttons with a single Play/Pause toggle in `src/nnvisu/static/index.html`
- [x] T013 [US3] Implement Play/Pause toggle logic in `src/nnvisu/static/main.js`
- [x] T014 [US3] Implement instant visual clear of decision map on model reset in `src/nnvisu/static/main.js`

## Phase 6: User Story 4 - Training History Seekbar (P3)
**Goal**: Scrub through training evolution.
**Independent Test**: Training for 100 steps and then scrubbing the seekbar shows past decision maps.

- [x] T015 [P] [US4] Add history seekbar (range input) to UI in `src/nnvisu/static/index.html`
- [x] T016 [US4] Implement history recording buffer with 256 snapshot limit and pruning logic in `src/nnvisu/static/main.js`
- [x] T017 [US4] Implement seekbar scrubbing to update canvas display from history buffer in `src/nnvisu/static/main.js`

## Phase 7: User Story 5 - Branding and Metadata (P3)
**Goal**: Professional attribution and usage instructions.
**Independent Test**: Footer displays Jan Švec's info; Header shows "nnvisu" and usage steps.

- [x] T018 [P] [US5] Update header title and add "How-to" instructions in `src/nnvisu/static/index.html`
- [x] T019 [P] [US5] Implement footer with author information and GitHub link in `src/nnvisu/static/index.html`

## Phase 8: Polish & Cross-Cutting Concerns
**Goal**: Final verification and styling.

- [x] T020 Finalize UI layout and responsiveness in `src/nnvisu/static/style.css`
- [x] T021 Ensure all backend tests pass for weight adaptation in `tests/unit/test_model_adaptation.py`
- [x] T022 Conduct manual end-to-end verification of all user stories.
