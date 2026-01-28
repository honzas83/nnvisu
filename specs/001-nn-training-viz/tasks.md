---
description: "Task list for Neural Network Training Visualization feature"
---

# Tasks: Visualise Neural Network Training

**Input**: Design documents from `/specs/001-nn-training-viz/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/websocket.md

**Tests**: Tests are included where critical for logic verification, following the "Test-First" principle.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure (backend/src, frontend/src) per plan
- [x] T002 Initialize Python environment with `requirements.txt` (tornado, numpy, torch) in backend/
- [x] T003 [P] Configure `ruff.toml` and `mypy.ini` in backend/ for code quality
- [x] T004 [P] Create basic `index.html` and `style.css` skeleton in frontend/src/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Setup Tornado application entry point in `backend/src/app.py`
- [x] T006 Implement Websocket Handler skeleton in `backend/src/handlers.py`
- [x] T007 Define shared protocol constants/schemas in `backend/src/protocol.py`
- [x] T008 Setup frontend main script and Websocket connection in `frontend/src/main.js`
- [x] T009 Implement basic Canvas rendering loop in `frontend/src/main.js`

**Checkpoint**: Backend server runs, Frontend connects via WS, Canvas renders blank/test frame.

---

## Phase 3: User Story 1 - Define Training Data (Priority: P1) 🎯 MVP Increment 1

**Goal**: Users can add points to the canvas and see them rendered.

**Independent Test**: Click on canvas -> Point added to backend -> Point rendered on frontend.

### Implementation

- [x] T010 [P] [US1] Define `TrainingExample` class in `backend/src/logic/model.py`
- [x] T011 [US1] Implement `ADD_POINT` and `CLEAR_POINTS` handling in `backend/src/handlers.py`
- [x] T012 [P] [US1] Implement In-Memory storage for points in `backend/src/app.py` (or state manager)
- [x] T013 [P] [US1] Implement click event listener in `frontend/src/main.js` to send `ADD_POINT`
- [x] T014 [US1] Implement `drawPoints` function in `frontend/src/main.js` to render points by class
- [x] T015 [US1] Add UI controls (buttons/radio) to select current Class (0/1) in `frontend/src/index.html`

**Checkpoint**: User can place points of different classes.

---

## Phase 4: User Story 2 - Train and Visualize (Priority: P1) 🎯 MVP Complete

**Goal**: Users can train the model and see the decision boundary evolve.

**Independent Test**: Add points -> Start Training -> Watch loss decrease and background change.

### Backend Implementation

- [x] T016 [P] [US2] Define `NeuralNetwork` (PyTorch model) in `backend/src/logic/model.py`
- [x] T017 [US2] Implement `Trainer` class in `backend/src/logic/trainer.py` (step, epoch, loss)
- [x] T018 [US2] Implement `ClassificationMap` generation (grid prediction) in `backend/src/logic/trainer.py`
- [x] T019 [US2] Implement `START_TRAINING` and `STOP_TRAINING` handlers in `backend/src/handlers.py`
- [x] T020 [US2] Implement background training loop (asyncio task) to broadcast `TRAINING_STATUS`
- [x] T021 [US2] Implement throttling and broadcasting of `MAP_UPDATE` (Base64) in `backend/src/handlers.py`

### Frontend Implementation

- [x] T022 [P] [US2] Add "Start" and "Stop" buttons to `frontend/src/index.html`
- [x] T023 [US2] Implement handler for `TRAINING_STATUS` to update epoch/loss display in `frontend/src/main.js`
- [x] T024 [US2] Implement handler for `MAP_UPDATE` to draw decision boundary on Canvas in `frontend/src/main.js`

### Testing

- [x] T025 [P] [US2] Unit test: `Trainer` runs one step and updates weights in `backend/tests/unit/test_trainer.py`

**Checkpoint**: Full end-to-end training and visualization loop is functional.

---

## Phase 5: User Story 3 - Refine and Retrain (Priority: P2)

**Goal**: Incremental training without resetting weights.

**Independent Test**: Train -> Stop -> Add Point -> Resume -> Training continues (loss doesn't jump to initial).

### Implementation

- [x] T026 [P] [US3] Ensure `Trainer` persists model instance between `START_TRAINING` calls in `backend/src/logic/trainer.py`
- [x] T027 [US3] Implement `RESET_MODEL` handler to explicitly re-init weights in `backend/src/handlers.py`
- [x] T028 [P] [US3] Add "Reset Model" button to `frontend/src/index.html`
- [x] T029 [US3] Update frontend controls state (disable config during training) in `frontend/src/main.js`

**Checkpoint**: User can pause, modify dataset, and continue training.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T030 Handle Websocket disconnection/reconnection gracefully in `frontend/src/main.js`
- [x] T031 Optimize `MAP_UPDATE` rendering (ensure offscreen canvas usage) if FPS < 10
- [x] T032 Add basic styling to UI controls in `frontend/src/style.css`
- [x] T033 Verify Code Quality (Run `ruff` and `mypy` on all backend code)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Phase 1. Blocks all stories.
- **User Story 1 (Phase 3)**: Depends on Phase 2.
- **User Story 2 (Phase 4)**: Depends on Phase 3 (needs points to train).
- **User Story 3 (Phase 5)**: Depends on Phase 4.

### Parallel Opportunities

- Frontend and Backend tasks within each phase can largely be done in parallel once the Protocol (T007) is defined.
- T003/T004 (Config/Skeleton) can run in parallel.
- T016 (Model def) and T022 (UI buttons) can run in parallel.

## Implementation Strategy

1. **Skeleton**: Get WS connection working (Phase 2).
2. **Data**: Get points on screen (Phase 3).
3. **Intelligence**: Connect PyTorch loop and Map broadcasting (Phase 4).
4. **Refinement**: Persistence and controls (Phase 5).
