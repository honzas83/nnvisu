# Research & Decisions: Multi-user Backend Refactor

**Feature**: `003-backend-refactor-multiuser`
**Created**: 2026-02-02

## 1. Python Packaging with Static Data

### Problem
We need to bundle the frontend (HTML/JS/CSS) inside the `nnvisu` Python package so it can be installed via `pip` and served by the backend.

### Research
- **Tools**: `setuptools` is the standard and fully supports `pyproject.toml` configuration.
- **Mechanism**: Use `[tool.setuptools.package-data]` to include non-python files.
- **Configuration**:
  ```toml
  [project]
  name = "nnvisu"
  version = "0.1.0"
  dependencies = ["tornado", "numpy", "torch"]
  
  [tool.setuptools]
  packages = ["nnvisu"]
  package-dir = {"" = "src"}
  
  [tool.setuptools.package-data]
  nnvisu = ["static/**/*"]
  ```

### Decision
Use **`setuptools`** with `pyproject.toml` configuration. It is the standard, requires no extra tools (like poetry/flit) for the user, and handles recursive package data well.

## 2. Serving Static Files from Package

### Problem
Tornado's `StaticFileHandler` needs a filesystem path. When installed as a package (possibly a zip/wheel), the static files might not be directly on the filesystem in a predictable way.

### Research
- **`importlib.resources` (Python 3.9+)**: The modern way to access package resources.
- **`importlib.resources.files(package)`**: Returns a `Traversable` object.
- **`as_file` context manager**: Can extract the resource to a temporary file/directory if it's in a zip, or return the path if it's on disk.
- **Tornado Compatibility**: Tornado expects a string path for `static_path`.

### Decision
Use **`importlib.resources.files("nnvisu").joinpath("static")`**.
Since `pip install` usually installs packages as directories (not zipped eggs) in modern environments, `str(files("nnvisu").joinpath("static"))` often works. However, to be robust:

```python
import importlib.resources
from pathlib import Path

# In app.py
def get_static_path():
    return importlib.resources.files("nnvisu").joinpath("static")
    # Note: Tornado accepts a pathlib.Path object in recent versions, or we convert to str()
```

## 3. Stateless Protocol Payload

### Problem
We need to send training data + weights on every request.

### Decision
- **Protocol**: JSON over WebSocket.
- **Structure**:
  ```json
  {
    "type": "train_step",
    "config": { "learning_rate": 0.01 },
    "network": { 
      "weights": [[...], ...], 
      "biases": [[...], ...] 
    },
    "data": [
      { "x": 0.1, "y": 0.5, "label": 0 },
      ...
    ]
  }
  ```
- **Response**:
  ```json
  {
    "type": "train_step_result",
    "network": { ... }, # Updated weights
    "loss": 0.123
  }
  ```
- **Rationale**: Keeping the backend purely functional (State In -> State Out) simplifies concurrency and testing. Bandwidth is acceptable for <1000 points.
