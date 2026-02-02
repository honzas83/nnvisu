# Data Model: GUI Dynamic Classes

## Entities

### 1. Snapshot (New)
A single frame of training history stored on the client.

| Field | Type | Description |
|-------|------|-------------|
| epoch | int | The training step number |
| mapData | ImageBitmap | The rendered decision map for this epoch |
| loss | float | The loss at this epoch |

### 2. Dataset (Existing - Modified)
The collection of points.

| Field | Type | Description |
|-------|------|-------------|
| x | float | Normalized x coordinate [-1, 1] |
| y | float | Normalized y coordinate [-1, 1] |
| label | int | Class index [0, N-1] |

## State Transitions (Frontend)

### Tool Selection
- **Draw Mode**: Selected class color (0-9). `Eraser` disabled.
- **Erase Mode**: `Eraser` enabled. Class selection visually inactive.

### Training History Subsampling
1. **RECORD**: Every `interval` steps, push `Snapshot` to `history`.
2. **LIMIT**: If `history.length > 256`:
    - Filter `history` to keep only even indices.
    - Set `interval = interval * 2`.

## Weight Adaptation Logic (Backend)

When `num_classes` changes:
- `weight_matrix`: shape `[num_classes, hidden_dim]`
- `bias_vector`: shape `[num_classes]`

Adaptation:
- **Addition**: `W_new = concat(W_old, random_row)`, `B_new = concat(B_old, zero)`
- **Removal**: `W_new = W_old[:new_size]`, `B_new = B_old[:new_size]`
