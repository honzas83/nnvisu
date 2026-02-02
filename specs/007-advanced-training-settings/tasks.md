# Tasks: Advanced Training Settings

**Feature Branch**: `007-advanced-training-settings`
**Plan File**: `specs/007-advanced-training-settings/plan.md`
**Status**: Done

## Implementation Strategy

We will follow a backend-first approach to ensure the PyTorch model and training logic are robust enough to handle dynamic hyperparameter switching. Once the backend foundations are in place, we will implement the "Advanced Options" UI panel and incrementally bind each setting (Activation, Optimizer, Batch Size, etc.) to the frontend state and WebSocket communication layer. Realtime updates and persistence will be verified at each step.

## Dependencies

1.  **Phase 2 (Foundational)** is a prerequisite for all subsequent phases as it modifies the core model and trainer interfaces.
2.  **Phase 3 (UI Infrastructure)** must be completed before any hyperparameter-specific UI tasks in Phases 4-6.
3.  Each user story implementation within Phases 4-6 includes both UI components and state binding.

---

## Phase 1: Setup
**Goal**: Initialize test environment for advanced training logic.

- [x] T001 Create `tests/unit/test_advanced_logic.py` to verify backend module switching and sampling.

## Phase 2: Foundational
**Goal**: Implement backend support for dynamic hyperparameters.

- [x] T002 Update `NeuralNetwork` in `src/nnvisu/logic/model.py` to support dynamic activation function selection and Dropout layer injection.
- [x] T003 Update `StatelessTrainer.train_step` in `src/nnvisu/logic/trainer.py` to support optimizer selection (SGD, ADAM, RMSProp) and L2 regularization (weight_decay).
- [x] T004 Implement random sampling logic for Batch Size in `StatelessTrainer.train_step` in `src/nnvisu/logic/trainer.py`.
- [x] T005 Update `NeuralWebSocket.handle_train_step` in `src/nnvisu/handlers.py` to correctly parse and pass the new config fields to the trainer.

## Phase 3: User Story 4 - Organized Advanced Interface (P2)
**Goal**: Create the collapsible container for advanced settings.

- [x] T006 [US4] Add the "Advanced Options" container (using `<details>` or custom toggle) below the canvas in `src/nnvisu/static/index.html`.
- [x] T007 [US4] Add styling for the Advanced panel and its internal layout in `src/nnvisu/static/style.css`.
- [x] T008 [US4] Implement panel expansion/collapse persistence using LocalStorage in `src/nnvisu/static/main.js`.

## Phase 4: User Story 1 & 2 - Core Hyperparameters (P1)
**Goal**: Enable activation selection and precise learning rate tuning.

- [x] T009 [P] [US1] Add Activation Function dropdown and Learning Rate numeric input to the Advanced panel in `src/nnvisu/static/index.html`.
- [x] T010 [US1] Bind Activation and LR inputs to `StateManager` and update the WS payload logic in `src/nnvisu/static/main.js`.
- [x] T011 [US1] Implement automatic model weight reset in `main.js` when the activation function is changed.

## Phase 5: User Story 3, 5 & 6 - Optimization & Regularization (P2)
**Goal**: Enable optimizer selection, L2 penalty, and batch size control.

- [x] T012 [P] [US5] Add Optimizer selection, Regularization coefficient, and Batch Size numeric inputs to `src/nnvisu/static/index.html`.
- [x] T013 [US5] Bind Optimizer, Regularization, and Batch Size inputs to `StateManager` and WS payloads in `src/nnvisu/static/main.js`.

## Phase 6: User Story 7 - Observe Dropout Effects (P3)
**Goal**: Implement dropout rate control.

- [x] T014 [US7] Add Dropout rate numeric input to the Advanced panel in `src/nnvisu/static/index.html`.
- [x] T015 [US7] Bind Dropout input to `StateManager` and WS payloads in `src/nnvisu/static/main.js`.

## Phase 7: Polish & Cross-Cutting Concerns
**Goal**: Final verification and code quality.

- [x] T016 Run `ruff check .` and `mypy .` to ensure type safety of the new config parsing and PyTorch logic.
- [x] T017 Conduct manual end-to-end verification of hyperparameter visual impacts using the browser.
