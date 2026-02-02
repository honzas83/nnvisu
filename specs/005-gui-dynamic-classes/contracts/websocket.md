# WebSocket API Contracts

## Messages

### Client -> Server

#### Train Step (Existing - Unchanged)
```json
{
  "type": "train_step",
  "config": { ... },
  "model": { "weights": [...], "biases": [...] },
  "data": [{ "x": 0.1, "y": 0.2, "label": 0 }, ...]
}
```
*Note*: The server will automatically detect the required output dimension from the maximum `label` in the `data` list.

### Server -> Client

#### Map Update (Existing - Unchanged)
```json
{
  "type": "map_update",
  "payload": {
    "width": 100,
    "height": 100,
    "format": "rgb",
    "data": "..."
  }
}
```

