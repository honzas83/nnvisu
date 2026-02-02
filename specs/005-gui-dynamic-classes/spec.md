# Feature Specification: GUI Dynamic Classes

**Feature Branch**: `005-gui-dynamic-classes`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "Next specification is mainly about GUI - I would like to have dynamic number of target classes. My idea is to have something like color palette with different colors. The number of classes is the number of unique colors. Implement also eraser tool for data point deletion. Implement also instant redraw of the output if the weights are reseted. The start stop training buttons should be merged together into Play/Pause-like button. And also the seekbar containing the training history (mainly the map) with adequately subsampled data would be helpful. In the bottom of the page add author: Jan Švec <honzas@kky.zcu.cz>, Department of Cybernetics, University of West Bohemia together with the link to project github. The page title should be like nnvisu and a brief description of function and how to use it."

## Clarifications

### Session 2026-02-02

- Q: How should the model handle architectural changes when the number of unique colors/classes in the dataset changes during active training? → A: Adapt existing weights by adding or removing only the corresponding rows/columns in the output layer's weight matrix.
- Q: What specific subsampling logic should be used for the training history seekbar? → A: Keep at most 256 snapshots; if exceeded, delete every 2nd snapshot and double the recording interval.
- Q: What visual feedback should the "Eraser" tool provide on the canvas? → A: Display a larger circular cursor to ease deletion.
- Q: How should the color palette be structured? → A: Provide a predefined set of 8-10 high-contrast categorical colors.
- Q: How should users switch between drawing and erasing tools? → A: Use mutually exclusive tool modes (select a color to draw, select eraser to delete).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dynamic Class Management (Priority: P1)

As a researcher, I want to create training data for an arbitrary number of classes by selecting different colors from a palette, so that I am not limited to a fixed set of pre-defined classes.

**Why this priority**: Core functionality enhancement that fundamentally changes how the user interacts with the model definition.

**Independent Test**: Verify that selecting a new color and adding points creates a new output class in the model architecture and training process.

**Acceptance Scenarios**:

1. **Given** the application is loaded, **When** I click a color in the palette, **Then** subsequent clicks on the canvas add data points of that color/class.
2. **Given** I have added points for 3 distinct colors, **When** I start training, **Then** the model output layer automatically adjusts to predict 3 classes.
3. **Given** training is active, **When** I add a point of a 4th new color, **Then** the model adapts (or resets) to handle the 4th class.

---

### User Story 2 - Data Point Eraser (Priority: P1)

As a user, I want to delete specific data points from the canvas using an eraser tool, so that I can correct mistakes or refine the dataset without clearing everything.

**Why this priority**: Essential for data manipulation and error correction.

**Independent Test**: Verify that clicking a point with the eraser tool removes it from the dataset and it disappears from the canvas.

**Acceptance Scenarios**:

1. **Given** existing data points on the canvas, **When** I select the "Eraser" tool and click on a point, **Then** that point is removed from the dataset and the visualization.
2. **Given** training is active, **When** I erase a point, **Then** the training continues using the updated dataset (excluding the removed point).

---

### User Story 3 - Training Flow Control (Priority: P2)

As a user, I want to control the training process using a single Play/Pause toggle button and see instant visual feedback when resetting the model, so that the interaction feels responsive and intuitive.

**Why this priority**: Improving UX and responsiveness.

**Independent Test**: Verify the button toggles state and label/icon, and that model reset clears the decision map immediately.

**Acceptance Scenarios**:

1. **Given** training is stopped, **When** I click "Play", **Then** training starts and the button changes to "Pause".
2. **Given** training is running, **When** I click "Pause", **Then** training stops and the button changes to "Play".
3. **Given** the model has a visible decision boundary, **When** I click "Reset", **Then** the decision boundary is immediately cleared or set to a random initialization state on the canvas.

---

### User Story 4 - Training History Seekbar (Priority: P3)

As a researcher, I want to scrub through the history of the training process using a seekbar, so that I can review how the decision boundary evolved over time.

**Why this priority**: Analytical feature for understanding training dynamics.

**Independent Test**: Verify that dragging the slider updates the displayed decision map to a previous state.

**Acceptance Scenarios**:

1. **Given** training has progressed for several epochs, **When** I pause and drag the seekbar to the middle, **Then** the canvas displays the decision boundary map from that earlier point in training.
2. **Given** I am scrubbing history, **When** I click "Play", **Then** training resumes from the current state (latest epoch).

---

### User Story 5 - Branding and Metadata (Priority: P3)

As a stakeholder, I want clear authorship attribution, project links, and a descriptive title on the page, so that users understand the tool's origin and purpose.

**Why this priority**: Professional presentation and attribution.

**Independent Test**: Verify the presence and correctness of the text and links in the page footer and header.

**Acceptance Scenarios**:

1. **Given** the page is loaded, **When** I scroll to the bottom, **Then** I see the author's name "Jan Švec", email, affiliation, and a working link to the GitHub repository.
2. **Given** the page is loaded, **When** I look at the header, **Then** I see the title "nnvisu" and a brief description of the tool.

--- 

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- **Class Removal**: If the user erases all points of a specific color, the system should effectively treat that class as non-existent or handle the missing label gracefully during training.
- **History Overflow**: If the training runs for a very long time, the history buffer should either cap at a maximum size (e.g., dropping oldest frames) or subsample more aggressively to prevent memory exhaustion.
- **Single Class Training**: If only one class (color) is present, the model training should still function (likely converging to predict that class everywhere) or warn the user.
- **Zero Data**: Clicking "Play" with no data points should either do nothing or show a "No data" warning.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a color palette with a predefined set of 8-10 high-contrast categorical colors to distinguish between classes.
- **FR-002**: The system MUST interpret the number of unique colors present in the dataset as the number of target classes. When this count changes, the system MUST incrementally adapt the model's output layer weights (adding or removing specific rows/columns) to preserve existing training progress where possible.
- **FR-003**: The system MUST provide an "Eraser" tool that removes data points when clicked or dragged over. The tool MUST display a large circular cursor to provide clear visual feedback of the deletion area.
- **FR-004**: The system MUST combine Start/Stop functionality into a single toggle button (Play/Pause).
- **FR-005**: The system MUST immediately redraw the visualization (clear or random noise) when the model weights are reset.
- **FR-006**: The system MUST record training history (decision maps) with a maximum capacity of 256 snapshots. If the limit is reached, the system MUST prune the history by deleting every second snapshot and doubling the recording interval to maintain a representative timeline within memory constraints.
- **FR-007**: The system MUST provide a slider (seekbar) to visualize the recorded training history when training is paused.
- **FR-008**: The system MUST display the specified author information and GitHub link in the page footer.
- **FR-009**: The system MUST display "nnvisu" and a usage description in the page title/header.
- **FR-010**: The system MUST implement mutually exclusive tool modes, where selecting a specific class color enables drawing and selecting the Eraser disables class drawing to enable deletion.

### Key Entities

- **Class/Color**: A distinct label for classification, mapped to a specific visual color.
- **History Frame**: A snapshot of the decision boundary map at a specific training epoch.
- **Dataset**: The collection of points (x, y, color/class).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can successfully train a model with 1, 2, 3, 4, or 5 distinct classes without page reload.
- **SC-002**: Eraser tool successfully removes points with <100ms latency.
- **SC-003**: Training history supports at least 50 snapshots without browser crash or significant lag.
- **SC-004**: Resetting weights updates the visual display in <200ms.