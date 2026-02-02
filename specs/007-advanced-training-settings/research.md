# Research: Advanced Training Settings

## 1. Activation Functions Mapping

**Goal**: Support Tanh, ReLU, Leaky ReLU, and GELU.

**Mapping**:
-   `tanh` -> `torch.nn.Tanh()`
-   `relu` -> `torch.nn.ReLU()`
-   `leaky_relu` -> `torch.nn.LeakyReLU(negative_slope=0.01)`
-   `gelu` -> `torch.nn.GELU()`

**Decision**: The `NeuralNetwork` class in `src/nnvisu/logic/model.py` should be updated to accept an `activation` string in its constructor and dynamically swap the activation module.

## 2. Optimizer Mapping & Regularization

**Goal**: Support SGD, ADAM, RMSProp and L2 Regularization.

**Mapping**:
-   `sgd` -> `torch.optim.SGD(model.parameters(), lr=lr, weight_decay=lambda)`
-   `adam` -> `torch.optim.Adam(model.parameters(), lr=lr, weight_decay=lambda)`
-   `rmsprop` -> `torch.optim.RMSprop(model.parameters(), lr=lr, weight_decay=lambda)`

**Decision**: The `StatelessTrainer.train_step` method in `src/nnvisu/logic/trainer.py` currently re-initializes the optimizer every step. It needs to be updated to select the optimizer class based on the `config`.

## 3. Mini-batch Training (Batch Size)

**Goal**: Support Batch Size control.

**Approach**:
-   If `batch_size >= num_points`, perform full batch gradient descent (current behavior).
-   If `batch_size < num_points`, randomly sample `batch_size` points from the data for each `train_step` call.

**Decision**: Implement sampling logic in `StatelessTrainer.train_step`.

## 4. Dropout Implementation

**Goal**: Support Dropout rate.

**Approach**: Add `nn.Dropout(p=dropout_rate)` after each activation function in the hidden layers. Note: `model.train()` and `model.eval()` must be called correctly during training vs map generation.

## 5. UI Placement & Persistence

**Goal**: Collapsible "Advanced" box below canvas with LocalStorage memory.

**Implementation**:
-   HTML: `<details>` and `<summary>` or a custom `div` with toggle.
-   CSS: Fixed width matching canvas, border-top or floating below.
-   JS: `localStorage.setItem('nnvisu_advanced_expanded', true/false)`.
-   Realtime: Attach `input` and `change` listeners to all fields to send `train_step` updates immediately.
