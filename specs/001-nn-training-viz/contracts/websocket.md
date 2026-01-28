# Websocket Protocol: Neural Viz

**Protocol**: JSON-based text messages.
**Encoding**: UTF-8.

## Client Messages (Requests)

### `ADD_POINT`
Adds a training example.
```json
{
  "type": "ADD_POINT",
  "payload": {
    "x": 0.5,
    "y": -0.2,
    "label": 0
  }
}
```

### `CLEAR_POINTS`
Removes all training examples.
```json
{
  "type": "CLEAR_POINTS"
}
```

### `START_TRAINING`
Begins or resumes the training loop.
```json
{
  "type": "START_TRAINING",
  "payload": {
    "learning_rate": 0.01
    // Future: hidden_layers config
  }
}
```

### `STOP_TRAINING`
Pauses the training loop.
```json
{
  "type": "STOP_TRAINING"
}
```

### `RESET_MODEL`
Re-initializes model weights (clears learning).
```json
{
  "type": "RESET_MODEL"
}
```

## Server Messages (Events)

### `TRAINING_STATUS`
Broadcasts current metrics (sent frequently, e.g., 10Hz).
```json
{
  "type": "TRAINING_STATUS",
  "payload": {
    "is_training": true,
    "epoch": 105,
    "loss": 0.045
  }
}
```

### `MAP_UPDATE`
Broadcasts the decision boundary grid (sent throttled, e.g., 5Hz).
```json
{
  "type": "MAP_UPDATE",
  "payload": {
    "width": 50,
    "height": 50,
    "data": "Base64EncodedStringOfBytes..." 
  }
}
```
*Note: `data` contains row-major class IDs (uint8).*
