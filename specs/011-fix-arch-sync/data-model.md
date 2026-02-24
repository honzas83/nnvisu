# Data Model: Architecture Synchronization

## Entities

### 1. NetworkArchitecture (Config)
Represents the structural definition of the model.
- `hidden_layers`: `List[int]` - Number of neurons per hidden layer (e.g., `[10, 5]`).
- `activation`: `str` - Activation function name (e.g., `"tanh"`, `"relu"`).
- `dropout`: `float` - Dropout probability (0.0 to 1.0).

### 2. NeuralModel (State)
The active PyTorch model in the backend.
- `id`: `int` - Unique memory identifier of the model instance.
- `weights`: `List[Tensor]` - Active weights per layer.
- `biases`: `List[Tensor]` - Active biases per layer.

## State Transitions

| Trigger | From State | To State | Side Effect |
|---------|------------|----------|-------------|
| UI Interaction (add/remove layer) | Training/Paused | Initializing | Stop Training Thread |
| Model Rebuild | Initializing | Ready | Re-init Weights/Biases |
| Data Update (classes change) | Ready | Adapting | Call `adapt_output_layer` |
