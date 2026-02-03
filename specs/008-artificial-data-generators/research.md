# Research: Artificial Data Generators

## Decision: NumPy implementation of scikit-learn generators

We will implement the following generators manually in `src/nnvisu/logic/generators.py` using NumPy to avoid adding `scikit-learn` as a dependency.

### 1. Blobs
- **Rationale**: Simplest distribution, useful for testing basic classification.
- **Implementation**: `X = np.random.randn(n_samples, 2) * cluster_std + centers[labels]`
- **Default**: `cluster_std=0.1`, `centers` distributed evenly in the [-1, 1] range.

### 2. Circles
- **Rationale**: Classic non-linearly separable dataset.
- **Implementation**:
  ```python
  linspace = np.linspace(0, 2 * np.pi, n_samples // 2, endpoint=False)
  outer = np.stack([np.cos(linspace), np.sin(linspace)], axis=1)
  inner = outer * factor
  X = np.vstack([outer, inner]) + np.random.normal(scale=noise, size=(n_samples, 2))
  ```
- **Default**: `factor=0.5`, `noise=0.05`. Always 2 classes.

### 3. Moons
- **Rationale**: Highly non-linear, popular for testing manifold learning and non-linear boundaries.
- **Implementation**:
  ```python
  linspace = np.linspace(0, np.pi, n_samples // 2)
  top = np.stack([np.cos(linspace), np.sin(linspace)], axis=1)
  bottom = np.stack([1 - np.cos(linspace), 1 - np.sin(linspace) - 0.5], axis=1)
  X = np.vstack([top, bottom]) + np.random.normal(scale=noise, size=(n_samples, 2))
  ```
- **Default**: `noise=0.05`. Always 2 classes.

### 4. Anisotropic
- **Rationale**: Tests how the classifier handles clusters with different orientations and aspect ratios.
- **Implementation**: 
  - Generate Blobs.
  - Transform: `X = X @ [[0.6, -0.6], [-0.4, 0.8]]`.
- **Default**: `cluster_std=0.1`.

### 5. Varied Variance
- **Rationale**: Tests how the classifier handles clusters with different densities.
- **Implementation**:
  - Generate Blobs but pass a list of `cluster_std` (e.g., `[0.05, 0.1, 0.2]`).
- **Default**: `cluster_stds=[0.05, 0.1, 0.15, 0.2, 0.25, 0.3]` (up to 6 classes).

## WebSocket Protocol Extensions

We need a new request type: `GENERATE_DATA`.

**Request**:
```json
{
  "type": "GENERATE_DATA",
  "distribution": "circles" | "moons" | "blobs" | "anisotropic" | "varied_variance",
  "num_classes": 3
}
```

**Response**:
```json
{
  "type": "DATA_GENERATED",
  "data": [
    {"x": 0.1, "y": 0.2, "label": 0},
    ...
  ]
}
```

## Alternatives Considered

### 1. Client-side generation (JavaScript)
- **Evaluation**: Would save a WebSocket roundtrip.
- **Rejected because**: 
  - Keeping generation on the backend ensures that the training data format is exactly what the backend expects.
  - Easier to implement consistently with Python/NumPy than porting logic to JS.
  - The latency of a WebSocket message is negligible for 200 points.

### 2. Using scikit-learn
- **Evaluation**: Very easy to implement.
- **Rejected because**: `scikit-learn` is a large dependency (~150MB+ with dependencies) just for 5 small functions. Manual implementation is ~50 lines of code.

## UI Design

- Add a `div.control-row` below the existing "Training data" title.
- Buttons will have icons or labels: `Circles`, `Moons`, `Blobs`, `Anisotropic`, `Varied`.
- Use CSS Flexbox to fit them in one row.
- Reuse the existing "Number of classes" selector if it exists, or add one if needed. (Wait, I should check `index.html`).
