# Data Model: Dense Probabilistic Grid

## Entities

### 1. Training Payload (Existing, Unchanged)
Represents the data sent from Client to Server to trigger a training step.

| Field | Type | Description |
|-------|------|-------------|
| type | string | "train_step" |
| config | object | Training configuration (learning rate, architecture) |
| model | object | Current model state (weights, biases) |
| data | list | List of training points {x, y, label} |

### 2. Map Update Payload (Modified)
Represents the visualization grid sent from Server to Client.

| Field | Type | Description |
|-------|------|-------------|
| type | string | "map_update" |
| payload | object | The grid data |

#### Payload Object

| Field | Type | Description |
|-------|------|-------------|
| width | int | Grid width (New: 100) |
| height | int | Grid height (New: 100) |
| format | string | Data format identifier (New: "rgb") |
| data | string | Base64 encoded RGB byte array. Length = width * height * 3. |

### 3. Class Colors (Static Configuration)
Colors used for backend blending, matched to frontend.

| Class ID | Hex | RGB |
|----------|-----|-----|
| 0 | #3498db | (52, 152, 219) |
| 1 | #e67e22 | (230, 126, 34) |
| 2 | #e74c3c | (231, 76, 60) |
