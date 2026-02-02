# Implementation Plan - Multi-user Backend Refactor

**Goal**: Refactor the codebase to support multiple concurrent users with browser-based state persistence, move the backend to the project root, and package the application as an installable Python module (`nnvisu`).

## Technical Context

### Current State
- **Structure**: Split `backend/` and `frontend/` directories.
- **State**: In-memory on the backend (not multi-user safe).
- **Communication**: WebSocket (Tornado).
- **Packaging**: None (running via `python src/app.py`).
- **Dependencies**: `tornado`, `numpy`, `torch`.

### Proposed Changes
- **Directory Structure**: Flatten `backend/src` to `src/nnvisu` in root. Move `frontend/src` to `src/nnvisu/static`.
- **State Management**: Frontend stores full state (weights, data) in `localStorage`. Backend becomes stateless.
- **Protocol**: Frontend sends state + data with every training step request.
- **Packaging**: Create `pyproject.toml` in root using `setuptools` (standard, flexible).
- **Entry Point**: `src/nnvisu/__main__.py` for `python -m nnvisu`.

### Unknowns & Risks
- **Performance**: Sending full weights + data (~1000 points) on every step might be heavy? (Clarified in spec as acceptable for "toy" datasets).
- **Packaging**: Best way to include non-python files (static assets) recursively in `pyproject.toml`? [NEEDS CLARIFICATION]
- **Tornado Static File Handling**: How to serve the bundled static files efficiently from within the package structure? [NEEDS CLARIFICATION]

## Constitution Check

### Principle I: High Assurance Code Quality
- **Impact**: Refactoring involves moving files. Mypy configuration must be updated to point to the new source root. Strict typing must be maintained in the new package structure.
- **Compliance**: Will run `ruff` and `mypy` on the new structure.

### Principle II: Realtime-First Architecture
- **Impact**: Stateless backend means larger payloads per WebSocket message.
- **Compliance**: Tornado is non-blocking. We need to ensure deserializing the larger JSON payload doesn't block the event loop for too long. (Async JSON parsing or thread pool might be needed if payloads get large, but for <1MB it should be fine).

### Principle III: Rigorous Testing Standards
- **Impact**: Existing tests are in `backend/tests`. They need to be moved to `tests/` and updated to import from the new `nnvisu` package.
- **Compliance**: Will migrate and run all tests. Will add a test for `python -m nnvisu` execution.

### Principle IV: User Experience Consistency
- **Impact**: User state is now persistent across reloads (improvement).
- **Compliance**: Frontend logic needs to handle "loading" state from local storage seamlessly on startup.

## Phase 0: Outline & Research

### 1. Research Tasks
- [ ] Research `pyproject.toml` configuration for including recursive static data files with `setuptools`.
- [ ] Research `importlib.resources` (Python 3.11+) pattern for locating static files inside an installed package for Tornado to serve.

### 2. Design Tasks
- [ ] Define the new JSON protocol schema for the "Stateless Training" messages.
- [ ] Define the `localStorage` key schema.

### 3. Decisions
- **Packaging Tool**: `setuptools` (via `pyproject.toml`) because it has mature support for package data and entry points.
- **Static Serving**: Use `tornado.web.StaticFileHandler` pointed at a path resolved via `importlib.resources`.

## Phase 1: Design & Contracts

### 1. Data Models
- **Frontend State**:
  - `nnvisu_config`: `{ architecture: [int], learningRate: float }`
  - `nnvisu_weights`: `{ layer_0_weights: [[float]], layer_0_bias: [float], ... }`
  - `nnvisu_data`: `[{ x: float, y: float, label: int }]`
- **WebSocket Protocol**:
  - Request: `{ type: "step", config: {...}, weights: {...}, data: [...] }`
  - Response: `{ type: "step_result", gradients: {...}, loss: float }` (Actually, better to return updated weights directly if backend does the step?) -> *Correction*: Spec says "computes gradients/updates". Returning updated weights is simpler for the frontend.

### 2. API Contracts
- **WebSocket**: `/ws` (Single endpoint).
- **HTTP**: `/` (Serves `index.html`), `/static/*` (Serves JS/CSS).

### 3. Agent Context
- Update `backend` context to reflect the new package structure and removal of `backend/` dir.

## Phase 2: Implementation Breakdown

### Step 1: Directory Restructure
- Create `src/nnvisu`.
- Move `backend/src/*` to `src/nnvisu/`.
- Move `frontend/src/*` to `src/nnvisu/static/`.
- Create `pyproject.toml`.

### Step 2: Packaging Logic
- Implement `src/nnvisu/__main__.py`.
- Update `app.py` to find static files dynamically.

### Step 3: Backend Logic Update (Stateless)
- Modify `logic/trainer.py` to accept state as argument instead of holding it.
- Remove stateful classes/globals in `app.py`.

### Step 4: Frontend Logic Update (Stateful)
- Implement `StateManager` class in JS to handle `localStorage`.
- Update `WebSocket` logic to send full state.

### Step 5: Testing & Cleanup
- Move and update tests.
- Verify `pip install .`.
- Remove `backend/` and `frontend/` roots.