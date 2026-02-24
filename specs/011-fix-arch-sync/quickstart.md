# Quickstart: Architecture Sync Verification

## Test Scenario

Verify that changes to the UI architecture are correctly reflected in the backend PyTorch model.

### Prerequisites

1.  Start the backend server: `python -m nnvisu`
2.  Open the UI in a modern web browser.

### Verification Steps

1.  **Add a Layer**:
    -   Click the "+" button to add a hidden layer.
    -   **Expected**: Backend logs should indicate a model rebuild with the additional layer.
    -   **Expected**: UI should receive an `architecture_synced` message.

2.  **Change Neuron Count**:
    -   Increase the neuron count of an existing layer.
    -   **Expected**: Backend model should re-initialize its weights for that layer.
    -   **Expected**: Training should restart from a loss value reflecting the new weights.

3.  **Active Training Interaction**:
    -   Start training.
    -   While training is active, remove a hidden layer.
    -   **Expected**: Training should automatically stop.
    -   **Expected**: Model should rebuild with the updated architecture.
    -   **Expected**: Training should be able to restart without errors.
