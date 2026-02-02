# WebSocket API Contracts

## Messages

### Client -> Server

#### Train Step (Modified)
Represents the updated training payload including advanced settings.

```json
{
  "type": "train_step",
  "config": {
    "learningRate": 0.01,
    "architecture": [10, 5],
    "activation": "tanh",
    "optimizer": "adam",
    "regularization": 0.001,
    "batchSize": 32,
    "dropout": 0.1
  },
  "model": { "weights": [...], "biases": [...] },
  "data": [{ "x": 0.1, "y": 0.2, "label": 0 }, ...]
}
```

- **activation**: one of ["tanh", "relu", "leaky_relu", "gelu"]
- **optimizer**: one of ["sgd", "adam", "rmsprop"]
- **regularization**: float >= 0 (maps to weight_decay)
- **batchSize**: int >= 0 (0 or null implies full batch)
- **dropout**: float [0, 1]

