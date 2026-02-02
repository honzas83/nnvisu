# Research: Usability Layout Refactor

## 1. UI Grouping & Logical Sections

**Goal**: Organize controls into "Training Data" and "Training & History" panels.

**Decision**: Use distinct `<fieldset>` or `<div>` containers with semantic headers (`<h3>`) to separate the two functional areas. This provides clear visual boundaries.

**Rationale**: Users should easily distinguish between data entry tools and model execution controls.

## 2. Descriptive Labeling (Architecture)

**Goal**: Replace "Arch" with "Network Architecture (Hidden Layers)" and provide examples.

**Decision**:
- Update label to "Network Architecture (Hidden Layers)".
- Use an `<i>` or `<span>` with smaller, muted text for the example: `(e.g., 10-5-2)`.
- Use a tooltip or a small "info" icon for further clarification: "Numbers represent neurons in each hidden layer, separated by dashes."

## 3. History & Status Integration

**Goal**: Constrain seekbar width and move status metrics (Epoch, Loss) into the same control group.

**Decision**:
- Set `max-width: 600px` (matching canvas width) for the seekbar container.
- Create a "Status Bar" component that sits immediately above or below the range input.
- Layout:
  ```text
  [ Epoch: 123 | Loss: 0.0456 ]
  [----------O----------------] (Seekbar)
  ```

**Rationale**: Integrating these elements reduces the distance the user's eyes must travel to see the results of scrubbing or active training.

## 4. Onboarding (How-to)

**Goal**: Brief guide below the title.

**Decision**: Use a simple ordered list (`<ol>`) with 3-4 steps.
1. Pick a color and click the canvas to add training points.
2. Press ▶ Train to start the neural network training.
3. Use the History slider to review previous decision maps.
4. Adjust the architecture or Reset the model to experiment.

## 5. Instant Redraw on Reset

**Goal**: Provide immediate visual feedback when weights are cleared or randomized.

**Decision**: The `resetModel` function in `main.js` will be updated to explicitly trigger a `map_update` from the server using the freshly initialized weights, rather than waiting for the next training iteration.

**Rationale**: This ensures the user sees the "blank slate" or random state of the model immediately upon clicking Reset, improving the perceived responsiveness of the application.
