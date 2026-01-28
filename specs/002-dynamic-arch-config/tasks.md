# Tasks: Dynamic Architecture & 3rd Class

**Branch**: `002-dynamic-arch-config` | **Spec**: [specs/002-dynamic-arch-config/spec.md](../spec.md)

## Phase 1: Setup
*Initialize feature context and verify environment.*

- [x] T001 Verify project structure and test environment (run existing tests) in `tests/`

## Phase 2: Foundational (Blocking)
*Core backend logic for dynamic architecture.*

- [x] T002 [P] Update `NeuralNetwork` class in `backend/src/logic/model.py` to accept `hidden_layers` list and `output_dim`
- [x] T003 [P] Implement `make_model` factory or update `__init__` in `backend/src/logic/model.py` to build `nn.Sequential` dynamically
- [x] T004 Create unit tests for dynamic model creation (valid/invalid inputs) in `backend/tests/unit/test_model_dynamic.py`

## Phase 3: User Story 1 - Define Hidden Layer Architecture (P1)
*Allow users to specify network structure.*

- [x] T005 [US1] Update `handlers.py` to parse `RESET_MODEL` payload for `hidden_layers` config
- [x] T006 [US1] Update `trainer.py` or app state to initialize model with new config on reset
- [x] T007 [P] [US1] Add architecture input field `<input id="arch-input">` to `frontend/src/index.html`
- [x] T008 [US1] Implement input validation (regex, limits) in `frontend/src/main.js`
- [x] T009 [US1] Trigger `RESET_MODEL` with payload on input blur/enter in `frontend/src/main.js`
- [x] T010 [US1] Verify architecture update via backend logs (manual test)

## Phase 4: User Story 2 - Visualize 3-Class Classification (P1)
*Support Red class and multi-class logic.*

- [x] T011 [P] [US2] Update `trainer.py` data generation to support 3 target classes
- [x] T012 [P] [US2] Update `NeuralNetwork` instantiation to use `output_dim=3` when data has 3 classes in `backend/src/logic/trainer.py`
- [x] T013 [P] [US2] Add "Class 2 (Red)" button to `frontend/src/index.html`
- [x] T014 [US2] Update `frontend/src/main.js` to handle `label=2` (Red) in point generation/sending
- [x] T015 [US2] Update `frontend/src/main.js` heatmap rendering to map class 2 to Red color
- [x] T016 [US2] Update `frontend/src/main.js` point rendering to color class 2 points Red

## Phase 5: Polish & Cross-Cutting
*Validation, limits, and cleanup.*

- [x] T017 Enforce soft limits (max 10 layers, 100 neurons) in `backend/src/handlers.py` (return error if exceeded)
- [x] T018 Ensure `CrossEntropyLoss` is used correctly for >2 classes in `backend/src/logic/trainer.py` (verify `nn.Linear` output is logits)
- [x] T019 Update `quickstart.md` if any steps changed during implementation

## Dependencies

1. **T002, T003** (Model Logic) must be done before **T005** (Handler Integration).
2. **T005** (Backend Support) must be done before **T009** (Frontend Trigger).
3. **T011** (Data Logic) must be done before **T015** (Visualization).

## Implementation Strategy
- **MVP**: Complete Phase 2 and Phase 3 to get dynamic architecture working with 2 classes first.
- **Increment**: Add Phase 4 to enable the 3rd class.
- **Final**: Apply limits and polish.
