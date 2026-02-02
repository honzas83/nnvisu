# Feature Specification: Advanced Training Settings

**Feature Branch**: `007-advanced-training-settings`  
**Created**: 2026-02-02  
**Status**: Draft  
**Input**: User description: "Now add Advanced box bellow the data canvas. Advanced options include: Selection of activation functions for hidden units (tanh, ReLU, Leaky ReLU and other), learning rate input box, weight regularization coefficient and other options, that are didacticaly important."

## Clarifications

### Session 2026-02-02

- Q: How should the model behave when the activation function is changed mid-training? → A: Automatically reset model weights to a random state.
- Q: What is the default display state of the "Advanced Options" panel? → A: Collapsed by default, with state remembered in local storage.
- Q: How should changes in the Advanced panel be applied? → A: Apply immediately when any field changes (realtime updates).
- Q: Which activation functions and optimizers should be supported in the Advanced panel? → A: Activation: tanh, ReLU, Leaky ReLU, GELU. Optimizer: SGD, ADAM, RMSProp.
- Q: Which additional neural network features should be included for didactic purposes? → A: Batch Size and Dropout.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Customize Activation Function (Priority: P1)

As a student, I want to switch between different activation functions (e.g., Tanh, ReLU, GELU) to observe how the mathematical properties of the hidden units affect the shape and smoothness of the decision boundaries.

**Why this priority**: Fundamental educational value for understanding neural network behavior.

**Independent Test**: Can be tested by switching between activations and verifying the change in decision boundary geometry.

**Acceptance Scenarios**:

1. **Given** a model is training with Tanh, **When** I select "ReLU" or "GELU" in the Advanced box, **Then** the subsequent decision maps show the corresponding transitions.
2. **Given** the Advanced panel is open, **When** I change the activation function, **Then** the model weights are automatically reset to a random initialization state.

---

### User Story 5 - Optimizer Selection (Priority: P2)

As a user, I want to switch between different optimizers (SGD, ADAM, RMSProp) to see how they handle gradient updates and convergence.

**Why this priority**: Teaches the importance of optimization algorithms in neural network training.

**Independent Test**: Verify that switching to SGD results in different training trajectories compared to ADAM.

**Acceptance Scenarios**:

1. **Given** the Advanced panel, **When** I select "SGD", **Then** the model training uses Stochastic Gradient Descent logic.

---

### User Story 6 - Control Batch Size (Priority: P2)

As a student, I want to adjust the batch size to understand the trade-off between the noisy updates of stochastic descent and the stable updates of batch descent.

**Why this priority**: Teaches a core concept of deep learning optimization.

**Independent Test**: Set batch size to 1 and verify that the decision boundary updates are more erratic compared to using the full dataset.

**Acceptance Scenarios**:

1. **Given** training is active, **When** I set batch size to 1, **Then** each training step uses only one randomly sampled data point.

---

### User Story 7 - Observe Dropout Effects (Priority: P3)

As a researcher, I want to apply Dropout to the hidden layers to observe how randomly disabling neurons during training improves generalization.

**Why this priority**: Demonstrates a common regularization technique visually.

**Independent Test**: Apply high dropout (e.g., 0.5) and verify that the decision boundary becomes more robust but potentially takes longer to converge.

**Acceptance Scenarios**:

1. **Given** training is active, **When** I set a non-zero dropout rate, **Then** neurons in the hidden layers are randomly deactivated during each forward pass.

---

### User Story 2 - Precision Learning Rate Tuning (Priority: P1)

As a researcher, I want to manually specify the learning rate so that I can experiment with convergence speed, stability, and the effects of high learning rates (e.g., oscillating loss).

**Why this priority**: Essential for controlling the training dynamics and teaching optimization concepts.

**Independent Test**: Can be tested by setting a very high learning rate and verifying that the loss fluctuates or the boundary "jumps" drastically between steps.

**Acceptance Scenarios**:

1. **Given** training is active, **When** I change the learning rate from 0.01 to 0.1, **Then** the loss metrics reflect faster (but potentially less stable) updates.
2. **Given** an invalid learning rate (e.g., -1), **When** I attempt to save/apply, **Then** the system reverts to a safe default or displays an error.

---

### User Story 3 - Weight Regularization Control (Priority: P2)

As a user, I want to adjust the weight regularization coefficient (L2 penalty) to see how penalizing large weights leads to simpler, more generalized decision boundaries.

**Why this priority**: Important for teaching the concept of overfitting and regularization.

**Independent Test**: Can be tested by placing many points in a complex pattern, applying high regularization, and verifying that the decision boundary becomes smoother and "less accurate" to the training data.

**Acceptance Scenarios**:

1. **Given** a dataset with noise, **When** I increase the regularization coefficient, **Then** the decision boundaries become less complex and more rounded.

---

### User Story 4 - Organized Advanced Interface (Priority: P2)

As a user, I want these technical hyperparameters grouped in an "Advanced" box below the canvas, so that the primary controls (Play/Pause, Palette) remain uncluttered.

**Why this priority**: UX improvement to maintain a clean interface for beginners while providing depth for advanced users.

**Independent Test**: Verify the existence and toggle-ability of the "Advanced" container.

**Acceptance Scenarios**:

1. **Given** the main dashboard, **When** I look below the canvas, **Then** I see an "Advanced Options" section (collapsed by default on first load).
2. **Given** the Advanced box is expanded, **When** I refresh the page, **Then** the box remains expanded.

---

### Edge Cases

- **Zero/Negative Hyperparameters**: What happens when the user enters 0 or negative values for learning rate or regularization? (Expected: Use absolute value or enforce a minimum epsilon).
- **Activation Change during Training**: Handled by automatically resetting weights to ensure numerical stability and consistent behavior with the new activation logic.
- **Extreme Regularization**: Setting lambda to a very high value (e.g., 1000) might effectively zero out all predictions.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide an "Advanced Options" panel located below the visualization canvas.
- **FR-002**: The system MUST allow selection of at least the following activation functions: Tanh, ReLU, Leaky ReLU, and GELU.
- **FR-003**: The system MUST provide a numeric input for the Learning Rate (default: 0.01).
- **FR-004**: The system MUST provide a numeric input for the Weight Regularization Coefficient (L2 Lambda, default: 0).
- **FR-005**: The system MUST apply hyperparameter changes immediately upon field modification (e.g., input change or selection) to provide realtime visual feedback.
- **FR-006**: The system MUST persist Advanced settings across model resets (unless the user explicitly clears configuration).
- **FR-007**: The system MUST validate numeric inputs to prevent training crashes due to NaN or Infinite values.
- **FR-008**: The system MUST automatically reset model weights to a random state whenever the hidden unit activation function is changed.
- **FR-009**: The system MUST persist the expanded/collapsed state of the Advanced panel in local storage.
- **FR-010**: The system MUST allow selection of at least the following optimizers: SGD, ADAM, and RMSProp.
- **FR-011**: The system MUST provide a numeric input for Batch Size (default: full dataset).
- **FR-012**: The system MUST provide a numeric input for Dropout rate (default: 0).

### Key Entities

- **Hyperparameters**: The set of configuration values (activation, learning rate, regularization) used by the trainer.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Model convergence behavior visibly changes when the learning rate is adjusted by an order of magnitude.
- **SC-002**: The "Advanced Options" panel does not obstruct the main canvas or palette controls.
- **SC-003**: Selection of different activation functions results in correct Pytorch module application on the backend.
- **SC-004**: Input validation prevents training from hanging if an empty or invalid string is entered into numeric fields.