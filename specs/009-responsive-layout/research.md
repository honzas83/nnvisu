# Research: Responsive Layout & Technical Fixes

## Decision 1: WebSocket Proxy URL Resolution
**Decision**: Use `window.location` to construct a path-aware WebSocket URL.
**Rationale**: Hardcoding `/ws` fails when the application is served behind a reverse proxy on a subpath (e.g., `/nnvisu/`). By using `window.location.pathname`, we ensure the WebSocket path is always relative to the application's base URL.
**Implementation**:
```javascript
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const path = window.location.pathname.replace(/\/$/, '');
const wsUrl = `${protocol}//${window.location.host}${path}/ws`;
```
**Alternatives considered**: 
- Hardcoding `wss://`: Rejected because it breaks local development on `http`.
- Using relative URLs: `new WebSocket('ws')` is not supported by standard WebSocket API in all browsers.

## Decision 2: CPU-only PyTorch
**Decision**: Explicitly set `device = torch.device("cpu")` in backend logic and update `pyproject.toml` to use the standard `torch` dependency while documenting the CPU-only requirement.
**Rationale**: While `pyproject.toml` can point to CPU-specific wheels, these are platform-dependent (e.g., `+cpu` for Linux). For a general-purpose library, it is safer to force the device in code to ensure consistency across environments without breaking installation on macOS (which uses Accelerate/MPS but often defaults to CPU anyway).
**Implementation**:
```python
# In logic/model.py and logic/trainer.py
self.device = torch.device("cpu")
self.model.to(self.device)
```
In `pyproject.toml`, we will keep `torch` but add a comment or use an optional dependency group if necessary. Given the request "add dependency on pytorch CPU-only", I will investigate if there's a specific `torch-cpu` package (there isn't a standard one on PyPI, it's usually handled via `--extra-index-url`).
**Alternatives considered**: 
- Using `torch-cpu`: Does not exist on standard PyPI.
- Platform-specific wheels in `pyproject.toml`: Too brittle for cross-platform support.

## Decision 3: Responsive CSS Grid Layout
**Decision**: Use a CSS Grid with a fixed-width left column and a flexible right column for wide screens (>1024px).
**Rationale**: Grid provides the most robust way to handle the two-column requirement while allowing the left column to scroll independently and the right column to remain fixed/sticky.
**Implementation**:
```css
@media (min-width: 1024px) {
    #app {
        display: grid;
        grid-template-columns: 400px 1fr;
        grid-template-areas: "sidebar main";
        height: 100vh;
        width: 100vw;
        max-width: none;
        margin: 0;
        border-radius: 0;
    }
    header, #controls, #advanced-options {
        grid-area: sidebar;
        overflow-y: auto;
        padding: 20px;
    }
    main {
        grid-area: main;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #f0f2f5;
    }
    canvas {
        position: sticky;
        top: 20px;
        max-height: 90vh;
        width: auto !important;
    }
}
```
**Alternatives considered**: 
- Flexbox: Harder to manage independent scrolling of one column while keeping the other fixed without nested scroll containers.

## Decision 4: Project Metadata Centralization
**Decision**: Use `importlib.metadata` (or `pkg_resources` fallback) to read version/author from `pyproject.toml` and expose via `nnvisu/__init__.py`.
**Rationale**: Avoids duplication of version strings across `pyproject.toml`, `index.html`, and `app.py`.
**Implementation**:
```python
# src/nnvisu/__init__.py
try:
    from importlib.metadata import version, metadata
except ImportError:
    from importlib_metadata import version, metadata

meta = metadata("nnvisu")
__version__ = meta["Version"]
__author__ = meta["Author"]
```
