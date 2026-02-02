# WebSocket Contract

**Endpoint**: `/ws`

## Overview
The WebSocket connection handles the main training loop. It follows a Request-Response pattern where the Client sends the full state, and the Server returns the result of one training step (updated state).

## Messages

### Client -> Server: `train_step`
Request to perform a single step of backpropagation.

```json
{
  "type": "train_step",
  "config": {
    "learningRate": 0.01,
    "architecture": [2, 4, 2],
    "activation": "tanh"
  },
  "model": {
    "weights": [[[0.1, ...], ...], ...],
    "biases": [[0.1, ...], ...]
  },
  "data": [
    { "x": 0.5, "y": -0.2, "label": 1 },
    ...
  ]
}
```

### Server -> Client: `step_result`
Successful completion of a training step.

```json
{
  "type": "step_result",
  "model": {
    "weights": [[[0.09, ...], ...], ...],
    "biases": [[0.11, ...], ...]
  },
  "metrics": {
    "loss": 0.452,
    "accuracy": 0.85
  }
}
```

### Server -> Client: `error`
Application level error.

```json
{
  "type": "error",
  "message": "Invalid network architecture match."
}
```
