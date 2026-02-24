# Tasks: Fix architecture synchronization between UI and network

**Feature Branch**: `011-fix-arch-sync`
**Implementation Plan**: `specs/011-fix-arch-sync/plan.md`

## Phase 1: Setup
Initialization and environment preparation.

- [X] T001 Verify project structure and run baseline tests with `pytest`
- [X] T002 Create integration test scaffold in `tests/integration/test_architecture_sync.py`

## Phase 2: Foundational
Prerequisites for architectural synchronization.

- [X] T003 Update `src/nnvisu/protocol.py` to include `update_architecture` and `architecture_synced` message types
- [X] T004 Refactor `src/nnvisu/logic/model.py` to ensure `NeuralNetwork` can be safely re-instantiated with new configurations
- [X] T005 [P] Implement `MSG_TYPE_UPDATE_ARCH` constant and related types in `src/nnvisu/protocol.py`

## Phase 3: User Story 1 - Synchronize Hidden Layers (P1)
Goal: Ensure adding/removing layers in UI reflects in the backend model.

- [X] T006 [P] [US1] Create unit test for model re-instantiation in `tests/unit/test_model_dynamic.py`
- [X] T007 [US1] Update `src/nnvisu/handlers.py` to handle `update_architecture` message by recreating the model
- [X] T008 [US1] Implement immediate sync trigger in `src/nnvisu/static/main.js` when layers are added/removed
- [X] T009 [US1] Verify hidden layer sync: Add a layer in UI and confirm backend model structure update

## Phase 4: User Story 2 - Synchronize Neuron Counts (P1)
Goal: Ensure changing neuron count in UI reflects in the backend model.

- [ ] T010 [P] [US2] Add unit test for neuron count updates in `tests/unit/test_model_dynamic.py`
- [X] T011 [US2] Ensure `src/nnvisu/handlers.py` correctly passes neuron counts to `NeuralNetwork` constructor
- [X] T012 [US2] Update UI state management in `src/nnvisu/static/state_manager.js` to emit sync messages on neuron count changes
- [X] T013 [US2] Verify neuron count sync: Change neurons in UI and confirm weight matrix dimension change in backend

## Phase 5: User Story 3 - Training State Consistency (P2)
Goal: Ensure training stops and resets safely on architecture change.

- [X] T014 [US3] Implement `handle_stop_training` call within the architecture update handler in `src/nnvisu/handlers.py`
- [X] T015 [US3] Update `src/nnvisu/logic/session.py` to safely handle model replacement while a trainer thread might be active
- [X] T016 [US3] Add integration test in `tests/integration/test_architecture_sync.py` verifying training stops on sync
- [X] T017 [US3] Verify state consistency: Change architecture during active training and confirm auto-stop and reset

## Phase 6: Polish & Cross-cutting Concerns
Validation, constraints, and final touches.

- [X] T018 [P] Enforce maximum constraints (10 layers, 100 neurons) in `src/nnvisu/handlers.py` validation logic
- [X] T019 [P] Implement visual "Syncing..." indicator or feedback in `src/nnvisu/static/index.html` and `main.js`
- [X] T020 Run final verification suite: `pytest` and manual check against `quickstart.md`

## Dependencies
- US1 and US2 are independent but both depend on Phase 2 Foundational tasks.
- US3 depends on US1 and US2 being partially implemented to test against active state.
- Phase 6 depends on all User Stories.

## Parallel Execution Examples
- **Setup & Foundational**: T001, T003, T005 can run in parallel if developers coordinate on protocol definitions.
- **US1 & US2**: T006 and T010 (unit tests) can be developed simultaneously.
- **Backend & Frontend**: T007 (backend handler) and T008 (frontend trigger) can be developed in parallel once protocol is defined.

## Implementation Strategy
- **MVP**: Focus on T001-T009 (Phase 1-3). Successfully syncing a hidden layer addition is the core "aha" moment.
- **Incremental**: Follow with neuron count sync (US2), then safety/stability (US3), and finally polish.
