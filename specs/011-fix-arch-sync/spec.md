# Feature Specification: Fix architecture synchronization between UI and network

**Feature Branch**: `011-fix-arch-sync`  
**Created**: 2026-02-24  
**Status**: Draft  
**Input**: User description: "Fix a bug, where the architecture change in UI is not reflected in the network."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Synchronize Hidden Layers (Priority: P1)

A user adds or removes a hidden layer using the UI controls. The system immediately updates the internal model structure so that the next training step uses the new number of layers.

**Why this priority**: Fundamental requirement. If layers don't sync, the visualization and the actual model diverge, making the tool useless for architecture experimentation.

**Independent Test**: Add a hidden layer in the UI -> Start training -> Verify (via logs or backend state) that the model now has the additional layer.

**Acceptance Scenarios**:

1. **Given** a network with 2 hidden layers, **When** the user adds a 3rd hidden layer in the UI, **Then** the internal model must be reconfigured to include 3 hidden layers.
2. **Given** a network with 2 hidden layers, **When** the user removes a hidden layer in the UI, **Then** the internal model must be reconfigured to include 1 hidden layer.

---

### User Story 2 - Synchronize Neuron Counts (Priority: P1)

A user adjusts the number of neurons in an existing hidden layer. The system updates the weight matrices and bias vectors of the internal model to match the new dimensions.

**Why this priority**: Core functionality. Neuron count is the primary way users tune model capacity.

**Independent Test**: Change a layer from 4 to 8 neurons -> Run one training iteration -> Confirm the operation succeeds without dimension mismatch errors.

**Acceptance Scenarios**:

1. **Given** a hidden layer with 4 neurons, **When** the user increases the count to 6 in the UI, **Then** the internal layer must be resized to 6 neurons and weights re-initialized.
2. **Given** a hidden layer with 4 neurons, **When** the user decreases the count to 2 in the UI, **Then** the internal layer must be resized to 2 neurons.

---

### User Story 3 - Training State Consistency (Priority: P2)

When the architecture changes, the system ensures the training state is consistent (e.g., resetting weights) so that the model doesn't attempt to use incompatible weights from the previous architecture.

**Why this priority**: Prevents runtime crashes and mathematical errors caused by shape mismatches between the UI state and the backend model.

**Independent Test**: Change architecture while training is paused -> Resume training -> Verify training starts fresh with the new architecture.

**Acceptance Scenarios**:

1. **Given** an active training session, **When** the user changes the architecture, **Then** the system MUST automatically stop training and reset the model to prevent crashes.

---

### Edge Cases

- **Rapid UI Changes**: User clicks "+" or "-" buttons rapidly. The system should handle these without race conditions or partial updates.
- **Empty Network**: What happens if the user removes all hidden layers? (Should fall back to a linear model or prevent removal).
- **Extreme Counts**: Handling very large numbers of neurons or layers that might exceed memory or cause UI lag.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST update the internal neural network structure whenever the number of hidden layers is modified in the UI.
- **FR-002**: System MUST update the internal neural network structure whenever the neuron count of any layer is modified in the UI.
- **FR-003**: System MUST re-initialize the network weights and biases immediately upon any architecture change to ensure mathematical consistency.
- **FR-004**: System MUST synchronize architecture changes to the backend immediately on every UI interaction to maintain state parity.
- **FR-005**: System MUST validate the new architecture configuration before applying it to the internal model, enforcing a maximum of 10 hidden layers and 100 neurons per layer.

### Key Entities *(include if feature involves data)*

- **Network Configuration**: Represents the structural definition of the network (layers, neurons per layer).
- **Neural Model**: The internal stateful object (e.g., PyTorch model) that performs the actual training and inference.
- **Sync Protocol**: The message format used to communicate architecture changes from the UI to the training backend.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Architecture changes in the UI are reflected in the backend model in under 100ms.
- **SC-002**: Zero "dimension mismatch" or "shape error" exceptions occur during training after an architecture change.
- **SC-003**: 100% of architecture configurations visible in the UI match the actual network structure being trained.
- **SC-004**: Users can successfully resume/start training within 2 clicks after any architecture modification.
