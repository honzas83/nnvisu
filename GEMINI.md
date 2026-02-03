# nnvisu Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-28

## Active Technologies
- N/A (In-memory training state) (002-dynamic-arch-config)
- Python 3.11+ + Tornado (WebSockets), PyTorch (Inference), NumPy (Matrix Ops) (004-dense-probabilistic-grid)
- N/A (In-memory) (004-dense-probabilistic-grid)
- Python 3.11+, JavaScript (ES6) + Tornado (Backend), PyTorch (Inference/Training), Browser Canvas API (Frontend) (005-gui-dynamic-classes)
- `localStorage` (Configuration/Data), In-memory (Training History) (005-gui-dynamic-classes)
- Python 3.11+, JavaScript (ES6) + Tornado, PyTorch, Browser Canvas API (006-usability-layout-refactor)
- N/A (UI Refactor) (006-usability-layout-refactor)
- Python 3.11+, JavaScript (ES6) + Tornado (WebSockets), PyTorch (NN Core), NumPy (007-advanced-training-settings)
- N/A (In-memory), LocalStorage for frontend settings (007-advanced-training-settings)
- Python 3.11+, JavaScript (ES6) + Tornado (WebSockets), NumPy (Mathematical distributions), PyTorch (Backend model), Browser Canvas API (Frontend rendering) (008-artificial-data-generators)
- Python 3.11+, JavaScript (ES6) + Tornado, PyTorch (CPU-only), NumPy, Browser Canvas API (009-responsive-layout)

- Python 3.11+ + Tornado (Web server/Websockets), NumPy (Data processing), PyTorch (Neural Network training - *Tentative, pending research*) (001-nn-training-viz)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.11+: Follow standard conventions

## Recent Changes
- 009-responsive-layout: Added Python 3.11+, JavaScript (ES6) + Tornado, PyTorch (CPU-only), NumPy, Browser Canvas API
- 008-artificial-data-generators: Added Python 3.11+, JavaScript (ES6) + Tornado (WebSockets), NumPy (Mathematical distributions), PyTorch (Backend model), Browser Canvas API (Frontend rendering)


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
