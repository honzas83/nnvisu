# Quickstart: Artificial Data Generators

## How to use

1. Open the **nnvisu** application.
2. Locate the **Training Data** section in the sidebar.
3. Observe the new row of buttons: **Circles**, **Moons**, **Blobs**, **Anisotropic**, and **Varied**.
4. Set the desired **Number of Classes** (default is 2 or 3 depending on distribution).
5. Click any distribution button.
6. The canvas will immediately populate with 200 points in that pattern.
7. Press **Train** to see how the model adapts to the new data.

## Implementation Notes for Developers

- Generators are located in `src/nnvisu/logic/generators.py`.
- WebSocket message handling is in `src/nnvisu/handlers.py`.
- UI updates are in `src/nnvisu/static/main.js` and `index.html`.
