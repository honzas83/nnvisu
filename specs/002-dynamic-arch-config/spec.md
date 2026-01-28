# Feature Specification: Dynamic Architecture & 3rd Class

**Feature Branch**: `002-dynamic-arch-config`  
**Created**: 2026-01-28  
**Status**: Draft  
**Input**: User description: "Now, add third class (red color) and inputbox for architecture definition (e.g. 2-10-5-3, 2D input, 3 target classes, 10 and 5 hidden units)."

## Clarifications

### Session 2026-01-28
- Q: How should the system handle the relationship between the architecture string and the number of classes/dimensions? → A: Input is fixed to 2D, output is fixed to the number of classes; the user input specifies hidden layers only (e.g., "10-5").
- Q: Should there be limits on the network complexity (depth/width) to prevent performance issues? → A: Yes, enforce a soft limit: max 100 neurons per layer and max 10 hidden layers.
- Q: When should the network architecture update trigger? → A: Re-initialize the network immediately on "Enter" key press or when the input field loses focus (blur).
- Q: What happens to current training progress when the architecture is updated? → A: Current training progress is cleared, and weights are re-initialized from scratch.
- Q: What happens when the number of target classes changes? → A: The network output layer is resized, and weights are immediately re-initialized from scratch to match the new dataset structure.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Define Hidden Layer Architecture (Priority: P1)

The user wants to define the hidden layers of the neural network (number of layers and neurons per layer) via a simple text input. The input and output layers are automatically handled by the system based on the 2D input and the number of target classes.

**Why this priority**: Essential for the educational/exploratory purpose of the tool; allows immediate feedback on complexity without requiring the user to manage input/output dimensions.

**Independent Test**: Can be tested by entering various strings (e.g., "5", "10-10") and verifying the model structure updates (e.g., to "2-5-3" or "2-10-10-3" for a 3-class problem).

**Acceptance Scenarios**:

1. **Given** the application is loaded, **When** the user locates the architecture input box, **Then** it should show a default value for hidden layers (e.g., "5").
2. **Given** a 3-class dataset, **When** the user types "8-4" and confirms, **Then** the application should re-initialize the neural network with: 2 input nodes, 8 neurons in 1st hidden layer, 4 neurons in 2nd hidden layer, and 3 output nodes.
3. **Given** an invalid input (e.g., "2-a-5"), **When** the user submits, **Then** the system should show an error or revert to the previous valid state.

---

### User Story 2 - Visualize 3-Class Classification (Priority: P1)

The user wants to see a third class of data points (Red) in the visualization to experiment with multi-class classification problems beyond binary choices.

**Why this priority**: Expands the problem space from binary to multi-class, a key concept in neural networks.

**Independent Test**: Can be tested by verifying the data generation logic produces 3 distinct groups and the visualization renders 3 distinct colors (including Red).

**Acceptance Scenarios**:

1. **Given** the architecture is set to output 3 classes (ends in "-3"), **When** the data is generated, **Then** there should be three distinct clusters of points.
2. **Given** the visualization is active, **When** the 3rd class points are rendered, **Then** they should be colored Red.
3. **Given** the model is training, **When** the decision boundaries are drawn, **Then** they should reflect regions for 3 different classes.

### Edge Cases

- **Invalid Architecture String**: User enters non-integers, negative numbers, or symbols other than hyphens.
- **Empty Hidden Layers**: User leaves the input empty or enters "0". This should result in a model with only input and output layers (Linear Perceptron, e.g., "2-3").
- **Dynamic Class Change**: If the user (in future) changes the number of classes from 2 to 3, the output layer of the network MUST automatically update to 3 without requiring user to re-enter hidden layers.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a text input field for hidden layer configuration.
- **FR-002**: System MUST parse the architecture string (format "H1-H2-...") to configure only the hidden layers of the Neural Network.
- **FR-003**: System MUST support a variable number of hidden layers (0 to N) based on input.
- **FR-004**: System MUST include a 3rd target class for data generation and visualization.
- **FR-005**: The 3rd class MUST be visualized with the color Red.
- **FR-006**: System MUST automatically append an output layer with a size equal to the current number of target classes.
- **FR-007**: System MUST automatically prepend an input layer with a size of 2 (fixed for 2D visualization).
- **FR-008**: System MUST validate input to ensure only positive integers and hyphens are accepted.
- **FR-009**: System MUST enforce limits: max 100 neurons per layer and max 10 hidden layers, providing an error message if exceeded.
- **FR-010**: System MUST trigger network re-initialization on "Enter" key press within the input field or when the field loses focus.
- **FR-011**: System MUST reset all weights and clear training progress (e.g., reset epoch counter/loss history) upon architecture change.
- **FR-012**: System MUST immediately resize the output layer and re-initialize weights from scratch if the number of target classes in the dataset changes.

### Key Entities *(include if feature involves data)*

- **HiddenArchConfig**: A string or list of integers representing ONLY the hidden layer sizes (e.g., `[10, 5]`).
- **FullArchitecture**: The resulting complete network structure (e.g., `[2, 10, 5, 3]`).
- **Dataset**: Now includes 3 labels (0, 1, 2) instead of just 2.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can successfully re-initialize the network with a new valid architecture in under 5 seconds.
- **SC-002**: Visualization clearly distinguishes 3 classes (colors are distinct: e.g., Blue, Orange, Red) to the naked eye.
- **SC-003**: Model successfully trains (loss decreases) on a 3-class dataset given an appropriate architecture (e.g., "2-10-3").