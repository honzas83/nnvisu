# Feature Specification: Artificial Data Generators

**Feature Branch**: `008-artificial-data-generators`  
**Created**: 2026-02-03  
**Status**: Draft  
**Input**: User description: "Now add second row to Training data section for generating artificial training data. Be inspired by sklearn's: https://scikit-learn.org/stable/auto_examples/cluster/plot_linkage_comparison.html . I expect to have at least 5 buttons for different distributions and also with different number of classes"

## Clarifications

### Session 2026-02-03
- Q: For distributions like "Circles" and "Moons" which are mathematically defined for two classes, how should the system behave if the user has selected a higher number of classes? → A: Ignore the selector for fixed-class distributions (force 2 classes).
- Q: Should the user be able to adjust the "noise" (random jitter) of the generated points, or should the system use a fixed, sensible default? → A: Fixed sensible default noise (keep UI clean).
- Q: Does the default sample size (e.g., 200 points) represent the total number of points across all classes, or the number of points generated per class? → A: Total points across all classes (consistent density).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Quick Test with Non-Linear Data (Priority: P1)

As a user, I want to quickly generate complex, non-linear data distributions (like circles or moons) so that I can evaluate how the neural network handles non-linearly separable datasets.

**Why this priority**: Core value of the tool is visualizing NN behavior on different data shapes. This provides instant complex data without manual drawing.

**Independent Test**: User clicks the "Circles" button; the UI and backend immediately update to show two concentric circles of data points.

**Acceptance Scenarios**:

1. **Given** the application is open, **When** the user clicks the "Circles" generator button, **Then** a new dataset consisting of two concentric circles is generated and displayed.
2. **Given** the application is open, **When** the user clicks the "Moons" generator button, **Then** a new dataset consisting of two interleaving half-circles is generated and displayed.

---

### User Story 2 - Testing Multi-Class Scalability (Priority: P2)

As a user, I want to select the number of classes for generated data so that I can observe how the model's decision boundaries evolve with more complex classification tasks.

**Why this priority**: Vital for testing the "Dynamic Classes" feature (005) and general model flexibility.

**Independent Test**: User sets class count to 4 and clicks "Blobs"; the UI shows four distinct clusters of points with four different labels.

**Acceptance Scenarios**:

1. **Given** a class count selector is set to 3, **When** the user clicks the "Blobs" generator button, **Then** three distinct isotropic Gaussian blobs are generated.
2. **Given** a class count selector is set to 5, **When** the user clicks the "Blobs" generator button, **Then** five distinct isotropic Gaussian blobs are generated.

---

### User Story 3 - Exploring Statistical Variance (Priority: P3)

As a user, I want to generate data with specific statistical properties (like anisotropic or varied variances) so that I can test the robustness of the classifier against different cluster shapes and densities.

**Why this priority**: Advanced testing for users who want to push the model's limits.

**Independent Test**: User clicks "Anisotropic"; the UI shows elongated clusters that are not perfectly circular.

**Acceptance Scenarios**:

1. **Given** the application is open, **When** the user clicks the "Anisotropic" generator button, **Then** clusters with elongated shapes are generated.
2. **Given** the application is open, **When** the user clicks the "Varied Variance" generator button, **Then** clusters with significantly different densities/spreads are generated.

---

### Edge Cases

- **What happens when the class count is set to a value higher than the model supports?** The generator should either cap the value or the system should handle the dynamic expansion of output layers gracefully.
- **How does system handle rapid clicks on different generators?** Each click should trigger a new generation, with the latest one taking precedence and cancelling previous (if any) pending updates.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a dedicated secondary row in the "Training data" UI section for artificial generators.
- **FR-002**: System MUST include buttons for at least 5 distinct distributions: Circles, Moons, Blobs, Anisotropic, and Varied Variance.
- **FR-003**: System MUST provide a mechanism (e.g., numeric input or dropdown) to specify the number of classes (clusters) for applicable generators (Blobs, Anisotropic, Varied Variance). For fixed-class distributions (Circles, Moons), the system MUST ignore this selector and always generate exactly 2 classes.
- **FR-004**: Clicking any generator button MUST immediately replace the current training dataset with the newly generated points.
- **FR-005**: The generated data MUST be automatically synchronized with the backend trainer to ensure consistent visualization of decision boundaries.
- **FR-006**: The generator MUST use a default sample size (e.g., 200 points) representing the TOTAL points across all classes. This ensures visual density remains consistent regardless of class count.
- **FR-007**: System MUST handle at least up to 6 classes for generated data, if the distribution supports it.
- **FR-008**: System MUST apply a fixed, sensible noise level (e.g., 0.05 to 0.1) to generated data to ensure realistic classification challenges without requiring manual configuration.

### Key Entities *(include if feature involves data)*

- **Data Generator**: A function or module that produces 2D points (x, y) with associated class labels based on a selected mathematical distribution.
- **Distribution Configuration**: Parameters for the generation process, including number of classes, noise level, and distribution type.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can generate a new dataset and see it rendered on the canvas in under 300ms from the button click.
- **SC-002**: The UI allows selecting between at least 5 different distributions without overcrowding the layout.
- **SC-003**: 100% of generated datasets are successfully sent to the backend and used for the next training iteration.
- **SC-004**: The number of classes in the generated data accurately reflects the user's selection in the UI.