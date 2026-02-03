# Tasks: Artificial Data Generators

**Feature**: Artificial Data Generators
**Plan**: [specs/008-artificial-data-generators/plan.md](plan.md)

## Implementation Strategy

We will implement the generators in priority order according to the user stories. Each user story will deliver a functional slice of the feature, including backend logic, WebSocket communication, and UI integration.

1. **MVP (US1)**: Concentric circles and interleaving moons. This provides the most visually striking non-linear datasets.
2. **Incremental (US2)**: Gaussian blobs with configurable class counts.
3. **Advanced (US3)**: Anisotropic and varied variance clusters.

## Phase 1: Setup

- [x] T001 Create initial backend generator module in `src/nnvisu/logic/generators.py`
- [x] T002 Update message protocol in `src/nnvisu/protocol.py` to include `generate_data` and `data_generated` types (if using TypedDict for routing)
- [x] T003 Create unit test file for generators in `tests/unit/test_generators.py`

## Phase 2: Foundational Backend Routing

- [x] T004 [P] Implement `generate_data` message handler in `src/nnvisu/handlers.py` to route to the appropriate generator
- [x] T005 [P] Implement basic error handling for unknown distribution types in `src/nnvisu/handlers.py`

## Phase 3: User Story 1 - Non-Linear Data (Circles & Moons) (Priority: P1)

**Goal**: Allow users to generate Circles and Moons datasets via UI buttons.
**Independent Test**: Clicking "Circles" button results in concentric circles rendered on the canvas; clicking "Moons" results in interleaving half-moons.

- [x] T006 [P] [US1] Implement `generate_circles` function in `src/nnvisu/logic/generators.py` (fixed 2 classes)
- [x] T007 [P] [US1] Implement `generate_moons` function in `src/nnvisu/logic/generators.py` (fixed 2 classes)
- [x] T008 [US1] Add unit tests for Circles and Moons in `tests/unit/test_generators.py`
- [x] T009 [US1] Add "Circles" and "Moons" buttons to `src/nnvisu/static/index.html` in a new "Generators" row
- [x] T010 [US1] Implement button click handlers in `src/nnvisu/static/main.js` to send `generate_data` message
- [x] T011 [US1] Implement `data_generated` response handler in `src/nnvisu/static/main.js` to update training data and trigger render

## Phase 4: User Story 2 - Multi-Class Scalability (Blobs) (Priority: P2)

**Goal**: Allow users to generate Gaussian blobs with a selectable number of classes.
**Independent Test**: Selecting "4 classes" and clicking "Blobs" results in 4 distinct clusters on the canvas.

- [x] T012 [P] [US2] Implement `generate_blobs` function in `src/nnvisu/logic/generators.py` supporting `num_classes` parameter
- [x] T013 [US2] Add unit tests for Blobs with varying class counts in `tests/unit/test_generators.py`
- [x] T014 [US2] Add "Number of classes" selector (dropdown or numeric input) to `src/nnvisu/static/index.html`
- [x] T015 [US2] Add "Blobs" button to `src/nnvisu/static/index.html`
- [x] T016 [US2] Update `main.js` to include the selected `num_classes` in the `generate_data` message for Blobs

## Phase 5: User Story 3 - Statistical Variance (Anisotropic & Varied Variance) (Priority: P3)

**Goal**: Allow users to generate Anisotropic and Varied Variance datasets.
**Independent Test**: Clicking "Anisotropic" shows elongated clusters; clicking "Varied" shows clusters with different densities.

- [x] T017 [P] [US3] Implement `generate_anisotropic` function in `src/nnvisu/logic/generators.py`
- [x] T018 [P] [US3] Implement `generate_varied_variance` function in `src/nnvisu/logic/generators.py`
- [x] T019 [US3] Add unit tests for Anisotropic and Varied distributions in `tests/unit/test_generators.py`
- [x] T020 [US3] Add "Anisotropic" and "Varied" buttons to `src/nnvisu/static/index.html`
- [x] T021 [US3] Update `main.js` to handle new distribution types and include `num_classes` where applicable

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T022 Apply styling for the new "Generators" row and buttons in `src/nnvisu/static/style.css`
- [x] T023 Implement debouncing or "latest-request-only" logic in `src/nnvisu/handlers.py` to handle rapid clicks
- [x] T024 Ensure consistent tooltips and labels across all new UI elements in `src/nnvisu/static/index.html`
- [x] T025 Verify responsiveness and layout integrity on smaller screens in `src/nnvisu/static/style.css`

## Dependencies

- Phase 2 depends on Phase 1
- Phase 3 (US1) depends on Phase 2
- Phase 4 (US2) depends on Phase 2
- Phase 5 (US3) depends on Phase 2
- Phase 6 depends on all previous phases

## Parallel Execution Examples

- **Backend Parallelism**: T006, T007, T012, T017, T018 (All backend generators can be implemented simultaneously once `generators.py` exists)
- **Frontend Parallelism**: T009, T014, T015, T020 (UI elements can be added to HTML independently)
- **Frontend Logic**: T010 and T011 can be worked on while backend is being implemented, assuming contract is followed.