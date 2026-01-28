# Data Model: Visualise Neural Network Training

**Branch**: `001-nn-training-viz`

## Entities

### TrainingExample
Represents a single user-defined data point in the 2D space.
- `id`: string (UUID) - Unique identifier.
- `x`: float - X coordinate (-1.0 to 1.0).
- `y`: float - Y coordinate (-1.0 to 1.0).
- `label`: int - Class identifier (0, 1, ...).

### ModelConfig
Configuration for the Neural Network.
- `hidden_layers`: List[int] - Number of neurons in each hidden layer (e.g., `[10, 5]`).
- `learning_rate`: float - Step size for the optimizer (e.g., `0.01`).
- `activation`: string - Activation function name (e.g., `ReLU`, `Tanh`).

### TrainingState
Ephemeral state of the training session.
- `is_training`: bool - Whether the training loop is active.
- `current_epoch`: int - Iteration count.
- `current_loss`: float - Most recent loss value.
- `weights_version`: int - Monotonically increasing counter for weight updates.

### ClassificationMap
The visual representation of the model's decision boundary.
- `width`: int - Grid width (e.g., 100).
- `height`: int - Grid height (e.g., 100).
- `class_ids`: bytes - Flattened array of predicted class IDs for each grid cell.
