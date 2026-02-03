# Tasks: Optimize Network Training

**Feature**: `010-optimize-network-training`
**Status**: Planned
**Total Tasks**: 16

## Phase 1: Setup

*Goal: Prepare the environment for stateful, threaded training.*

- [x] T001 Verify project structure and python environment validity `src/nnvisu/__init__.py`

## Phase 2: Foundational (Blocking)

*Goal: Establish the stateful session management and threading infrastructure required for decoupled training.*

- [x] T002 Create TrainingSession class for managing state and locking in `src/nnvisu/logic/session.py`
- [x] T003 Refactor StatelessTrainer to support threaded execution context in `src/nnvisu/logic/trainer.py`

## Phase 3: User Story 1 - Decoupled Training Performance (P1)

*Goal: Decouple the training loop from network I/O using a background thread.*

**Independent Test**:
- Run training with network throttling (e.g., 500kbps).
- Verify "Steps/Sec" in backend logs or UI remains high (>90% of unthrottled).
- Verify UI remains responsive.

**Implementation Tasks**:
- [x] T004 [US1] Update NeuralWebSocket to initialize and manage TrainingSession in `src/nnvisu/handlers.py`
- [x] T005 [US1] Implement 'start_training' command handler to spawn training thread in `src/nnvisu/handlers.py`
- [x] T006 [US1] Implement 'stop_training' command handler to safely stop thread in `src/nnvisu/handlers.py`
- [x] T007 [US1] Implement 'update_config' handler for thread-safe parameter updates in `src/nnvisu/handlers.py`
- [x] T008 [US1] Implement PeriodicCallback in handler to consume queue and send 'step_result' JSON updates in `src/nnvisu/handlers.py`
- [x] T009 [US1] Refactor frontend to send start/stop commands instead of driving the loop in `src/nnvisu/static/main.js`
- [x] T010 [US1] Update frontend state manager to handle asynchronous 'step_result' messages in `src/nnvisu/static/state_manager.js`

## Phase 4: User Story 2 - Adaptive Visualization Updates (P2)

*Goal: Implement binary protocol and frame dropping for visualization data.*

**Independent Test**:
- Connect via high-latency link.
- Observe visualization updating with latest state (jumping steps) rather than lagging.
- Verify payload size reduction via browser devtools.

**Implementation Tasks**:
- [x] T011 [US2] Implement generate_binary_map method for raw RGB output in `src/nnvisu/logic/trainer.py`
- [x] T012 [US2] Update handler to generate and send binary map updates periodically in `src/nnvisu/handlers.py`
- [x] T013 [US2] Implement binary message parsing (ArrayBuffer) in `src/nnvisu/static/main.js`
- [x] T014 [US2] Update canvas rendering logic to consume raw RGB data in `src/nnvisu/static/main.js`

## Phase 5: Polish & Cross-Cutting

*Goal: cleanup and final verification.*

- [x] T015 [P] Clean up any unused "stateless" logic or dead code in `src/nnvisu/handlers.py`
- [x] T016 Verify thread safety and absence of race conditions in `src/nnvisu/logic/session.py`

## Dependencies

1.  **Foundational (T002, T003)** must be completed first.
2.  **US1 (T004-T010)** depends on Foundational.
3.  **US2 (T011-T014)** depends on US1 (specifically the loop structure).
4.  **Polish (T015-T016)** runs last.

## Implementation Strategy

We will first build the backend `TrainingSession` and threading logic. Then we will refactor the communication to be server-driven (US1). Once the training loop is decoupled and running efficiently, we will optimize the data transport by switching the heavy visualization map to a binary format (US2).
