# Data Model: Dynamic Architecture

## Entities

### ArchitectureConfig
*Used to configure the neural network structure.*

| Field | Type | Description | Constraints |
|---|---|---|---|
| `hidden_layers` | `List[int]` | List of neuron counts for each hidden layer. | Max 10 layers, max 100 neurons each. Values > 0. |

### TrainingPoint
*Represents a single data point for training/visualization.*

| Field | Type | Description |
|---|---|---|
| `x` | `float` | X coordinate (-1 to 1). |
| `y` | `float` | Y coordinate (-1 to 1). |
| `label` | `int` | Class label (0, 1, or 2). |

### VisualizationMap
*Binary data sent to frontend for heatmap rendering.*

| Field | Type | Description |
|---|---|---|
| `width` | `int` | Width of the grid (e.g., 50). |
| `height` | `int` | Height of the grid (e.g., 50). |
| `data` | `bytes` | Base64 encoded array of class IDs (uint8). |
