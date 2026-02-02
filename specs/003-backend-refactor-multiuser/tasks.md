# Tasks: Multi-user Backend Refactor

**Feature Branch**: `003-backend-refactor-multiuser`
**Spec File**: `specs/003-backend-refactor-multiuser/spec.md`
**Plan File**: `specs/003-backend-refactor-multiuser/plan.md`

## Dependencies
- **Phase 1: Setup** (Project Restructure) -> Blocks all
- **Phase 2: Foundational** (Protocol definition) -> Blocks US1, US2
- **Phase 3: US1** (Core stateless logic) -> Blocks US2
- **Phase 4: US2** (Concurrent verification) -> Can start after US1 backend logic
- **Phase 5: US3** (Distribution) -> Blocks release

## Phase 1: Setup & Restructure
*Goal: Establish the new directory structure and package configuration.*

- [x] T001 Create new source directory structure `src/nnvisu/static` in project root
- [x] T002 Move `backend/src/*` contents to `src/nnvisu/`
- [x] T003 Move `frontend/src/*` contents to `src/nnvisu/static/`
- [x] T004 Create `pyproject.toml` in project root with `setuptools` configuration and dependencies (`tornado`, `numpy`, `torch`)
- [x] T005 [P] Move `backend/tests` to `tests/` and update import statements to use `nnvisu` package
- [x] T006 Remove legacy `backend/` and `frontend/` directories
- [x] T007 Create `src/nnvisu/__init__.py` to expose package interface

## Phase 2: Foundational
*Goal: Define protocols and shared schemas for stateless communication.*

- [x] T008 [P] Define `TrainingPayload` and `TrainingResult` TypedDicts/dataclasses in `src/nnvisu/protocol.py` matching `contracts/websocket.md`
- [x] T009 [P] Update `src/nnvisu/logic/model.py` to support initializing model state from dictionary (weights/biases)

## Phase 3: User Story 1 - Stateless Training Session
*Goal: Implement stateless backend logic and frontend persistence.*
*Independent Test: Reload page and verify state restoration; train step sends full state.*

- [x] T010 [US1] Refactor `src/nnvisu/logic/trainer.py` to be stateless (accept `model`, `data`, `optimizer` state in `train_step` method)
- [x] T011 [US1] Implement `StateManager` class in `src/nnvisu/static/js/state_manager.js` (or `main.js` refactor) to handle `localStorage` read/write for `nnvisu_config`, `nnvisu_weights`, `nnvisu_data`
- [x] T012 [US1] Update `src/nnvisu/app.py` `WebSocketHandler` to deserialize `train_step` message and reconstruct `TrainingContext`
- [x] T013 [US1] Update `src/nnvisu/app.py` `WebSocketHandler` to execute stateless training step and return `step_result`
- [x] T014 [US1] Update frontend WebSocket logic in `src/nnvisu/static/main.js` to construct `train_step` payload from local state
- [x] T015 [US1] Update frontend WebSocket logic in `src/nnvisu/static/main.js` to handle `step_result` and update local weights/metrics

## Phase 4: User Story 2 - Isolated Execution
*Goal: Ensure concurrent requests are handled independently.*
*Independent Test: Two tabs with different data/weights training simultaneously without interference.*

- [x] T016 [US2] Verify and ensure `src/nnvisu/app.py` uses no global state for training (audit `app.py` globals)
- [x] T017 [P] [US2] Add integration test `tests/integration/test_concurrency.py` simulating two simultaneous WebSocket connections with different data

## Phase 5: User Story 3 - Python Package Installation
*Goal: Make the application installable and executable as a module.*
*Independent Test: `pip install .` and `python -m nnvisu` works.*

- [x] T018 [US3] Create `src/nnvisu/__main__.py` entry point that invokes `app.py:main`
- [x] T019 [US3] Update `src/nnvisu/app.py` to locate static files using `importlib.resources` instead of relative paths
- [x] T020 [US3] Update HTML title in `src/nnvisu/static/index.html` to include "nnvisu"
- [x] T021 [US3] Verify `pyproject.toml` includes `[tool.setuptools.package-data]` for recursive static file inclusion

## Phase 6: Polish & Cross-Cutting
*Goal: Cleanup and code quality standards.*

- [x] T022 [P] Update `mypy.ini` (or `pyproject.toml` config) to point to new `src` root
- [x] T023 Run `ruff check . --fix` to ensure code style compliance in new structure
- [x] T024 Run `mypy .` and fix any type errors resulting from refactor

## Implementation Strategy
1. **MVP Scope**: Phases 1, 2, and 3 are the MVP. They deliver the working refactored app.
2. **Parallelism**: Phase 2 tasks can run parallel to Phase 1 cleanup. Frontend (T011, T014, T015) and Backend (T010, T012, T013) tasks in Phase 3 can technically proceed in parallel if the protocol (Phase 2) is strictly agreed upon.
