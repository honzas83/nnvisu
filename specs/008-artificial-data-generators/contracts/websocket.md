# WebSocket Contract: Artificial Data Generation

## Message Types

### 1. `GENERATE_DATA` (Client -> Server)
Request to generate a new dataset.

**Payload**:
```json
{
  "type": "generate_data",
  "distribution": "circles",
  "num_classes": 2
}
```

- `distribution`: One of `circles`, `moons`, `blobs`, `anisotropic`, `varied_variance`.
- `num_classes`: Integer [2, 8]. Ignored for `circles` and `moons`.

### 2. `DATA_GENERATED` (Server -> Client)
Response containing the newly generated points.

**Payload**:
```json
{
  "type": "data_generated",
  "data": [
    {"x": 0.5, "y": -0.2, "label": 0},
    {"x": -0.1, "y": 0.8, "label": 1}
  ]
}
```

## Error Handling
If an invalid distribution is requested, the server SHOULD return an `error` message type.
```json
{
  "type": "error",
  "message": "Invalid distribution: unknown_type"
}
```
