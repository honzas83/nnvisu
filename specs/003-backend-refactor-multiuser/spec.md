# Feature Specification: Multi-user Backend Refactor

**Feature Branch**: `003-backend-refactor-multiuser`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "Now, we will refactor the code, move everything from backend subdir into the root. At the same time, we will assume, that the app can be used by more users. Therefore, the user state will be stored in the browser local storage. The user will have a unique, signed ID to interact with the backend."

## Clarifications

### Session 2026-02-02
- Q: Storage Strategy? → A: **Full State in Browser**. Browser stores all state (weights, configuration). Backend is stateless; it performs calculations (backpropagation) on data/weights provided via the active WebSocket connection.
- Q: Identity Mechanism? → A: **No Persistent ID**. The "Signed User ID" requirement is removed. User isolation is handled implicitly by the uniqueness of the active WebSocket connection.
- Q: Data Ownership? → A: **Browser-Hosted Data**. The browser stores and sends the training data (generated via point-and-click, max ~1000 samples) along with the weights.
- Q: Local Storage Schema? → A: **Multi-Key Storage**. State is fragmented into separate keys (e.g., `weights`, `data`, `config`) for more efficient partial updates.
- Q: Installation & Execution? → A: **Pip Installable**. The application must be installable via `pip install "git repo"` and executable via `python -m nnvisu`.
- Q: Frontend Distribution? → A: **Bundled**. Frontend files are included in the `nnvisu` package data and served by the backend server directly from the package installation directory.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Stateless Training Session (Priority: P1)

As a user, I want my training configuration and state to be saved in my browser, so that I can resume my work later or reload the page without losing progress, even though the backend does not store my data.

**Why this priority**: Defines the core "Full State in Browser" architecture.

**Independent Test**: Configure a network, reload page -> Verify configuration is restored from Local Storage.

**Acceptance Scenarios**:

1. **Given** a user has modified the neural network configuration (weights, architecture), **When** they reload the page, **Then** the application restores the exact state from Local Storage keys.
2. **Given** a user connects to the backend, **When** they trigger a training step, **Then** the frontend sends the current weights and the collected click-and-point data (up to ~1000 samples) to the backend via WebSocket.
3. **Given** the backend receives a calculation request, **When** it computes the gradients/updates, **Then** it returns them to the *same* WebSocket connection and discards the state.

### User Story 2 - Isolated Execution (Priority: P1)

As a user, I want my training calculations to be isolated from other users, so that my results are not affected by others' activities.

**Why this priority**: Essential for multi-user support in a stateless environment.

**Independent Test**: Open two tabs. Set different weights in each. Step training in both. Verify results differ and correspond to respective inputs.

**Acceptance Scenarios**:

1. **Given** two users connected simultaneously via different WebSockets, **When** they send requests, **Then** the backend processes them independently using only the data provided in each respective connection payload.

### User Story 3 - Python Package Installation (Priority: P2)

As a developer/user, I want to install the application using standard Python tools, so that I can run it easily on my machine.

**Why this priority**: Improves accessibility and standardizes distribution.

**Independent Test**: Run `pip install .` in the root, then `python -m nnvisu` -> Verify server starts and web UI is accessible.

**Acceptance Scenarios**:

1. **Given** a Python environment, **When** I run `pip install <repo_url>`, **Then** all dependencies are installed and the `nnvisu` package is registered.
2. **Given** the package is installed, **When** I run `python -m nnvisu`, **Then** the backend server starts and serves the frontend at a local address.

---

### Edge Cases

- What happens if the WebSocket disconnects during a calculation? (Result is lost, Client must retry).
- What happens if the payload (Weights + Data) is too large for a single WebSocket frame? (Need fragmentation or size limits; ~1000 samples should fit comfortably).
- Package installation conflicts: Ensure `setup.py`/`pyproject.toml` correctly specifies dependencies to avoid environment breakage.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System structure MUST have all backend source code located in the project root, removing the `backend/` subdirectory.
- **FR-002**: The Backend MUST be stateless, storing no user-specific data between requests.
- **FR-003**: The Frontend MUST persist state (Neural Network weights, configuration, click-generated training data) in the browser's Local Storage using a multi-key approach.
- **FR-004**: The Frontend MUST transmit the complete necessary state (weights, data) to the Backend via WebSocket for training calculations.
- **FR-005**: The Backend MUST use the active WebSocket connection to identify the context for the response (request-response pattern).
- **FR-006**: Existing application functionality (NN training visualization) MUST remain functional after the directory refactor.
- **FR-007**: The system MUST support multiple simultaneous WebSocket connections processing independent data.
- **FR-008**: The application MUST be packaged as a standard Python package named `nnvisu`.
- **FR-009**: The package MUST be installable using `pip` directly from the git repository.
- **FR-010**: The application MUST be executable using the command `python -m nnvisu`.
- **FR-011**: The HTML title of the web application MUST include "nnvisu".
- **FR-012**: Frontend assets (HTML, JS, CSS) MUST be bundled within the Python package as package data.

### Key Entities *(include if feature involves data)*

- **App State**: Fragmented session data (Weights, Architecture, Click-Data) stored in the Browser across multiple Local Storage keys.
- **Training Payload**: The transient data structure sent over WebSocket containing Model State + Training Data for calculation.
- **Python Package (nnvisu)**: The distributable unit of the software.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of user configuration changes are persisted to Local Storage immediately.
- **SC-002**: `backend/` directory is removed from the codebase.
- **SC-003**: Application passes all existing regression tests after refactor.
- **SC-004**: System successfully handles 2+ concurrent users performing training steps without state cross-contamination.
- **SC-005**: Successful execution of `python -m nnvisu` after a clean `pip install`.
- **SC-006**: Web page title correctly displays "nnvisu".

## Assumptions

- "Data/Weights uploaded" implies the payload size is manageable for frequent WebSocket transmission (e.g., small toy datasets or batched updates).
- No server-side persistence (database/files) is required for user data.
- Dataset size is capped at approximately 1000 samples.
- The user has a working Python 3.11+ environment for installation.