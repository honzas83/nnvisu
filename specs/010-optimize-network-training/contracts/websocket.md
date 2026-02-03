# WebSocket Protocol Definitions

## Overview
The protocol is moving from a strictly request-response JSON format to a mixed JSON/Binary asynchronous flow.

## JSON Commands (Client -> Server)

### `start_training`
Starts the background training loop.

```json
{
  "type": "start_training"
}
```

### `stop_training`
Stops the background training loop.

```json
{
  "type": "stop_training"
}
```

### `update_config`
Updates hyperparameters on the fly.

```json
{
  "type": "update_config",
  "payload": {
    "learningRate": 0.01,
    "batchSize": 32,
    "regularization": 0.001
    // ... other config keys
  }
}
```

### `reset`
Resets the model (re-initializes weights).

```json
{
  "type": "reset"
}
```

## Server Updates (Server -> Client)

### `step_result` (JSON)
Sent periodically (e.g., 30fps) containing the latest loss and minimal status.

```json
{
  "type": "step_result",
  "metrics": {
    "loss": 0.123,
    "accuracy": 0.95
  },
  "step": 1500
}
```

### `map_update` (Binary)
Sent periodically, potentially at a lower rate than `step_result`.

**Format:**
`[TYPE: 1 byte] [WIDTH: 2 bytes] [HEIGHT: 2 bytes] [RGB DATA: W*H*3 bytes]`

- **TYPE**: `0x01` (Map Update)
- **WIDTH/HEIGHT**: Unsigned 16-bit integers (Little Endian)
- **RGB DATA**: Raw bytes, row-major order.
