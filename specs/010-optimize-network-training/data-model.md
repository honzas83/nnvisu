# Data Model: Optimize Network Training

## Backend Entities

### TrainingSession

A stateful container for a single client's training environment.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique session ID (UUID). |
| `model` | `NeuralNetwork` | The current PyTorch model instance. |
| `data` | `List[DataPoint]` | The current dataset. |
| `config` | `dict` | Training configuration (learning rate, architecture, etc.). |
| `training_active` | `bool` | Flag indicating if the background training thread is running. |
| `lock` | `threading.Lock` | Mutex to protect model access between training and visualization threads. |
| `update_queue` | `queue.Queue` | Queue for passing status updates to the main thread (optional, or use shared state). |

### Protocol Updates

#### Binary Message: Map Update
Replaces the JSON `map_update` with base64 payload.

**Structure (Little Endian):**
- **Header**: 1 byte (Message Type, e.g., `0x01` for Map Update)
- **Metadata**:
  - `uint16`: Width
  - `uint16`: Height
- **Body**:
  - `Height * Width * 3` bytes: RGB Data (Raw)

#### JSON Command: Start Training
Client -> Server

```json
{
  "type": "start_training"
}
```

#### JSON Command: Stop Training
Client -> Server

```json
{
  "type": "stop_training"
}
```

#### JSON Command: Update Config
Client -> Server. Updates the live training configuration.

```json
{
  "type": "update_config",
  "config": {
    "learningRate": 0.03,
    "batchSize": 10
    // ...
  }
}
```
