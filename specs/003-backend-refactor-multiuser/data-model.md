# Data Model: Multi-user Backend Refactor

**Feature**: `003-backend-refactor-multiuser`

## Frontend Entities (Local Storage)

### `nnvisu_app_state`
Global configuration for the session.

| Field | Type | Description |
|-------|------|-------------|
| `learningRate` | `float` | The current learning rate for training. |
| `batchSize` | `int` | (Optional) Future proofing, currently effectively full batch. |
| `isPlaying` | `boolean` | Whether the training loop is currently active. |

### `nnvisu_architecture`
Defines the structure of the neural network.

| Field | Type | Description |
|-------|------|-------------|
| `layers` | `List[int]` | Array of integers representing neuron count per layer (e.g., `[2, 4, 2]`). |
| `activation` | `string` | Activation function name (e.g., "tanh", "relu"). |

### `nnvisu_model`
The trainable parameters of the network.

| Field | Type | Description |
|-------|------|-------------|
| `weights` | `List[List[List[float]]]` | 3D array: Layer -> Input Neuron -> Output Neuron weights. |
| `biases` | `List[List[float]]]` | 2D array: Layer -> Neuron biases. |

### `nnvisu_data`
The training dataset.

| Field | Type | Description |
|-------|------|-------------|
| `points` | `List[Point]` | List of training examples. |

#### `Point`
| Field | Type | Description |
|-------|------|-------------|
| `x` | `float` | X coordinate (normalized -1 to 1). |
| `y` | `float` | Y coordinate (normalized -1 to 1). |
| `label` | `int` | Class label (0 or 1). |

## Backend Entities (Transient)

### `TrainingContext`
Derived from the WebSocket message, exists only during calculation.

| Field | Type | Description |
|-------|------|-------------|
| `model` | `PyTorch Module` | Reconstructed model from weights/config. |
| `data` | `Tensor` | Training batch tensor. |
| `optimizer` | `Optimizer` | Configured optimizer (stateless step). |
