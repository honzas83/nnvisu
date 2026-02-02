# Data Model: Advanced Training Settings

## Entities

### 1. Training Configuration (Modified)
Represents the hyperparameters used for model reconstruction and training.

| Field | Type | Description |
|-------|------|-------------|
| learningRate | float | Step size for weight updates. Default: 0.01. |
| architecture | list | Hidden layer sizes (e.g., [10, 5]). |
| activation | string | Selection: 'tanh', 'relu', 'leaky_relu', 'gelu'. |
| optimizer | string | Selection: 'sgd', 'adam', 'rmsprop'. |
| regularization | float | L2 weight decay coefficient. Default: 0. |
| batchSize | int | Number of points per step. 0 means full batch. |
| dropout | float | Dropout probability [0, 1]. |

## State Transitions (Frontend)

### Hyperparameter Update
1. **User Action**: Change value in Advanced panel.
2. **Persistence**: Save new value to `StateManager`.
3. **Application**: 
    - If `activation` changed: Trigger model reset.
    - Else: Apply to subsequent `train_step` payloads.

## Logic (Backend)

### Model Reconstruction
`NeuralNetwork(hidden_layers, output_dim, activation, dropout)`
- Builds layers using the specified activation function.
- Injects `nn.Dropout` if `dropout > 0`.

### Optimization Selection
`StatelessTrainer.train_step(model, data, config)`
- Extracts `optimizer`, `learningRate`, `regularization`, `batchSize`.
- Samples `batchSize` points from `data`.
- Initializes the chosen `torch.optim` instance.
