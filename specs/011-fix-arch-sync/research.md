# Research: Architecture Synchronization Mechanics

## Findings

### 1. Model Re-initialization Strategy
**Decision**: Full object recreation of `NeuralNetwork` is the most reliable path.
**Rationale**: PyTorch layers have fixed dimensions once created. While individual weights can be resized (as seen in `adapt_output_layer`), changing the entire architecture (number of layers and their connections) is cleaner and less error-prone by recreating the `NeuralNetwork` instance.
**Alternatives**: Manually manipulating `nn.Sequential` to add/remove layers. Rejected as complex and hard to maintain compared to recreation.

### 2. WebSocket Message Protocol
**Decision**: Add a new `update_architecture` message type.
**Rationale**: Current `update_config` is generic and used for hyperparameters (LR, regularization). A dedicated architecture message ensures the backend knows when a structural reset (and weight re-init) is required versus a simple parameter update.
**Message Schema**:
```json
{
  "type": "update_architecture",
  "payload": {
    "hidden_layers": [10, 5, 2],
    "activation": "tanh"
  }
}
```

### 3. State Consistency during Training
**Decision**: Use `handle_stop_training()` before applying structural changes.
**Rationale**: The `StatefulTrainer` runs in a separate thread. Modifying the `session.model` while the trainer is running could lead to `RuntimeError: Tensor shape mismatch` or `Segmentation Fault` if parameters are accessed during recreation.
**Action**: When `update_architecture` is received:
1. Stop training thread.
2. Re-create `NeuralNetwork` with new config.
3. Re-initialize weights.
4. Notify UI that sync is complete.

## Decisions
- Backend will enforce max 10 layers / 100 neurons.
- Architecture sync will always reset training progress (weights/biases).
- Sync will happen immediately on every UI interaction (add/remove layer or change neuron count).
