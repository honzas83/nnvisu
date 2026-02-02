# Quickstart: Advanced Training Settings

## New Features

1.  **Advanced Options Box**: Located below the canvas.
2.  **Activations**: Tanh, ReLU, Leaky ReLU, GELU.
3.  **Optimizers**: SGD, ADAM, RMSProp.
4.  **L2 Regularization**: Weight decay coefficient.
5.  **Mini-batching**: Specify batch size.
6.  **Dropout**: Hidden layer neuron deactivation.

## Verification Steps

1.  **Test Activation Reset**:
    - Add data points.
    - Start training.
    - Change activation from `tanh` to `ReLU`.
    - Verify that the model resets (boundaries change drastically) immediately.

2.  **Test Batch Size (Stochasticity)**:
    - Set `Batch Size` to 1.
    - Set `Learning Rate` to 0.1.
    - Start training.
    - Observe the "shaking" or noisy decision boundaries.

3.  **Test Regularization**:
    - Add a complex data pattern.
    - Set `Regularization` to a high value (e.g., 0.1).
    - Observe the boundaries becoming smoother and less complex over time.

4.  **Test Persistence**:
    - Expand the `Advanced Options` box.
    - Refresh the page.
    - Verify the box remains expanded and settings are restored.
