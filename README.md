# nnvisu: Neural Network Training Visualizer

A real-time web application to visualize the training process of a neural network on a 2D dataset. Users can interactively define training examples, observe the evolving decision boundaries, and refine the model through incremental training.

![Application Screenshot](screenshot.png)

## Features

- **Interactive Data Definition**: Add points to a 2D canvas with different classes.
- **Real-time Visualization**: Watch the classification regions change as the model learns.
- **Incremental Training**: Pause, add more data, and resume training from the previous state.
- **High Performance**: Uses Tornado for low-latency communication and HTML5 Canvas for smooth rendering.

## Tech Stack

- **Backend**: Python, Tornado, PyTorch, NumPy
- **Frontend**: Vanilla JavaScript, HTML5 Canvas, CSS3
- **Dev Tools**: Ruff, Mypy

## Getting Started

### Prerequisites

- Python 3.11+
- Web Browser (Chrome, Firefox, Safari, or Edge)

### Installation

1. Clone the repository.
2. Install dependencies (CPU-only recommended):
   ```bash
   pip install -r requirements.txt
   ```

**Alternative: Install directly from Git**
To install the CPU-only version directly from GitHub without cloning:
```bash
pip install "git+https://github.com/honzas83/nnvisu.git" --extra-index-url https://download.pytorch.org/whl/cpu
```

### Running the Application

1. Start the server:
   ```bash
   python -m nnvisu
   ```
2. Open your browser and navigate to:
   ```
   http://localhost:8888
   ```

## Usage

1. **Select Class**: Use the buttons to toggle between Class 0 (Blue) and Class 1 (Orange).
2. **Add Points**: Click on the canvas to place training examples.
3. **Start Training**: Click "Start Training" to begin the optimization process.
4. **Refine**: Click "Stop", add more points if needed, and click "Start" again to continue training.
5. **Reset**: Use "Reset Model" to clear weights and start over.

## License

MIT
