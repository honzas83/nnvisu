# Feature Specification: Usability Layout Refactor

**Feature Branch**: `006-usability-layout-refactor`  
**Created**: 2026-02-02  
**Status**: Draft  
**Input**: User description: "Now, we will improve usability. In the @screenshot.png is the current visual. Make two sections: (1) related to training data and (2) related to training and history. Instead of Arch: use something more descriptive with an example and what does it mean. Add simple howto bellow the header. The history slider is too wide. The Status can be somehow integrated with the history."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Organized Control Interface (Priority: P1)

As a researcher, I want the UI controls to be logically grouped into "Data" and "Training" sections, so that I can quickly find the tools relevant to my current task.

**Why this priority**: Improves mental mapping of the application's features and reduces visual clutter.

**Independent Test**: Can be tested by visually verifying that buttons and inputs are contained within labeled sections.

**Acceptance Scenarios**:

1. **Given** the application is loaded, **When** I look at the controls, **Then** I see two distinct sections labeled "Training Data" and "Training & History".
2. **Given** the sections are present, **When** I use data tools (palette, eraser), **Then** they are found within the "Training Data" section.

---

### User Story 2 - Descriptive Model Configuration (Priority: P1)

As a user, I want a clearer explanation of the "Arch" input, so that I understand how to configure the neural network layers correctly.

**Why this priority**: Essential for usability as "Arch" is a technical shorthand that may not be intuitive to all users.

**Independent Test**: Verify the label change and the presence of an example in the UI.

**Acceptance Scenarios**:

1. **Given** the training configuration section, **When** I look at the architecture input, **Then** the label is descriptive (e.g., "Network Architecture (Hidden Layers)") and includes an example (e.g., "e.g., 10-5").

---

### User Story 3 - Instant Onboarding (Priority: P2)

As a new user, I want a brief how-to guide visible on the page, so that I can immediately understand how to start using the tool without searching for documentation.

**Why this priority**: Lowers the barrier to entry for first-time users.

**Independent Test**: Verify the existence of the how-to section below the header.

**Acceptance Scenarios**:

1. **Given** the page header, **When** the application loads, **Then** a "How to use" section is displayed below the title with clear, concise steps.

---

### User Story 4 - Compact History & Status Integration (Priority: P2)

As a researcher, I want the training status and history controls to be integrated and visually balanced, so that I can monitor progress while reviewing history.

**Why this priority**: Optimizes screen real estate and connects related information (current state vs historical state).

**Independent Test**: Verify the seekbar width and the placement of status metrics (Epoch/Loss).

**Acceptance Scenarios**:

1. **Given** the training history section, **When** I look at the seekbar, **Then** its width is constrained to match the canvas or another reasonable limit.
2. **Given** the history controls, **When** training is active or paused, **Then** the current Epoch and Loss metrics are displayed adjacent to or integrated with the history seekbar.

### Edge Cases

- **Small Screens**: How does the dual-section layout wrap or stack on mobile/narrow viewports? (Default: Stack vertically).
- **Empty History**: How does the status integration look when training hasn't started yet? (Default: Display "Epoch: 0 | Loss: N/A").
- **Invalid Architecture Input**: If the user enters text that doesn't match the "10-5" pattern, clear error feedback should still be provided.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The UI MUST be divided into two primary control panels: "Training Data" and "Training & History".
- **FR-002**: The "Training Data" panel MUST contain the color palette, tool selection (Eraser), and "Clear Data" button.
- **FR-003**: The "Training & History" panel MUST contain the Play/Pause button, Architecture input, Reset button, and History Seekbar.
- **FR-004**: The label for network configuration MUST be updated to "Network Architecture (Hidden Layers)" or a similarly descriptive phrase.
- **FR-005**: The architecture input field MUST have a placeholder or adjacent text providing an example (e.g., "10-5-2").
- **FR-006**: A concise "How to use" instruction list MUST be added immediately below the main header title.
- **FR-007**: The CSS for the history seekbar MUST be updated to cap its maximum width (e.g., `max-width: 600px`).
- **FR-008**: The training metrics (Status, Epoch, Loss) MUST be relocated from the footer to the "Training & History" control section to provide better context.
- **FR-009**: The system MUST immediately redraw the decision boundary visualization when the model weights are reset, providing instant feedback to the user.

### Key Entities

- **Control Panel**: A UI container grouping related tools and inputs.
- **How-to Section**: A text block providing user instructions.
- **Integrated Status Display**: A UI component showing realtime metrics (Epoch, Loss) within the training control flow.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of control elements are contained within one of the two defined panels.
- **SC-002**: The "How to use" section is legible and contains no more than 4-5 brief steps.
- **SC-003**: The history seekbar width is reduced by at least 30% compared to the previous full-width implementation (or capped to canvas width).
- **SC-004**: Users can view Epoch and Loss information without scrolling to the bottom of the page if the canvas is large.