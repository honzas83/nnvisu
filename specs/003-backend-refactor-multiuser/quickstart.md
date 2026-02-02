# Quickstart: Multi-user Backend Refactor

**Feature**: `003-backend-refactor-multiuser`

## Development Setup

The project structure has changed. There are no longer separate `backend` and `frontend` directories at the root.

### 1. Installation (Editable Mode)

Install the package in editable mode to work on the code:

```bash
# From the project root
pip install -e .
```

### 2. Running the Server

Run the application as a Python module:

```bash
python -m nnvisu
```

Access the UI at: `http://localhost:8888`

### 3. Running Tests

Tests have been consolidated in the `tests/` directory (or `src/nnvisu/tests` depending on final placement, but `pytest` at root is standard).

```bash
pytest
```

### 4. Code Quality

Run checks on the new structure:

```bash
ruff check .
mypy .
```

## Frontend Development

The frontend files are now located in `src/nnvisu/static`.
- **HTML**: `src/nnvisu/static/index.html`
- **JS**: `src/nnvisu/static/main.js`
- **CSS**: `src/nnvisu/static/style.css`

Edits to these files require a page reload in the browser. No build step is required (vanilla JS).
