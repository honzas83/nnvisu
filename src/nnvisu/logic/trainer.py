import base64
from typing import List

import numpy as np
import torch
from torch import nn, optim

from nnvisu.logic.model import NeuralNetwork
from nnvisu.protocol import DataPoint

class StatelessTrainer:
    GRID_WIDTH = 100
    GRID_HEIGHT = 100

    # Class colors matching frontend (RGB)
    CLASS_COLORS = [
        [52, 152, 219],  # #3498db Blue
        [230, 126, 34], # #e67e22 Orange
        [231, 76, 60],  # #e74c3c Red
        [155, 89, 182], # #9b59b6 Purple
        [46, 204, 113], # #2ecc71 Green
        [241, 196, 15], # #f1c40f Yellow
        [121, 85, 72],  # #795548 Brown
        [52, 73, 94]    # #34495e Navy
    ]

    def __init__(self) -> None:
        self.criterion = nn.CrossEntropyLoss()

    def train_step(self, model: NeuralNetwork, data: List[DataPoint], config: dict) -> float:
        """
        Perform a single training step.
        Note: Optimizer state is not preserved between steps in this stateless design.
        """
        if not data:
            return 0.0

        # Hyperparameters from config
        learning_rate = config.get("learningRate", 0.01)
        optimizer_name = config.get("optimizer", "adam").lower()
        regularization = config.get("regularization", 0.0)
        batch_size = config.get("batchSize", 0)

        # Batch sampling
        if batch_size > 0 and batch_size < len(data):
            indices = np.random.choice(len(data), batch_size, replace=False)
            batch = [data[i] for i in indices]
        else:
            batch = data

        # Prepare batch tensors
        X = torch.tensor([[p['x'], p['y']] for p in batch], dtype=torch.float32)  # noqa: N806
        y = torch.tensor([p['label'] for p in batch], dtype=torch.long)

        # Re-initialize optimizer (stateless)
        opt_class = {
            'sgd': optim.SGD,
            'adam': optim.Adam,
            'rmsprop': optim.RMSprop
        }.get(optimizer_name, optim.Adam)

        optimizer = opt_class(model.parameters(), lr=learning_rate, weight_decay=regularization)

        model.train() # Set to train mode for dropout
        optimizer.zero_grad()
        outputs = model(X)
        loss = self.criterion(outputs, y)
        loss.backward()
        optimizer.step()

        return float(loss.item())

    def generate_map(self, model: NeuralNetwork, width: int = GRID_WIDTH, height: int = GRID_HEIGHT) -> str:
        """Generate classification map as base64 string (RGB bytes)."""
        model.eval() # Set to eval mode to disable dropout
        # Create grid
        # x: -1 to 1, y: -1 to 1
        x = np.linspace(-1, 1, width)
        y = np.linspace(1, -1, height) # Top-down for image
        xv, yv = np.meshgrid(x, y)

        # Flatten and convert to tensor
        grid_points = np.stack([xv.flatten(), yv.flatten()], axis=1)
        X_grid = torch.tensor(grid_points, dtype=torch.float32)  # noqa: N806

        # Predict probabilities
        with torch.no_grad():
            outputs = model(X_grid)
            # Apply softmax to get posterior probabilities
            probs = torch.softmax(outputs, dim=1) # [N, num_classes]

        num_classes = probs.shape[1]
        
        # Prepare color matrix [num_classes, 3]
        # Ensure we have enough colors defined
        colors = np.array(self.CLASS_COLORS)
        if num_classes > len(colors):
            # Fallback for extra classes: repeat last color or use random?
            # For this feature we assume 3 classes as per spec.
            extra = np.random.randint(0, 255, size=(num_classes - len(colors), 3))
            colors = np.vstack([colors, extra])
        else:
            colors = colors[:num_classes]

        # Calculate weighted average of colors
        # [N, num_classes] @ [num_classes, 3] -> [N, 3]
        blended_colors = probs.numpy() @ colors
        
        # Convert to bytes
        rgb_bytes = blended_colors.astype(np.uint8)
        return base64.b64encode(rgb_bytes.tobytes()).decode('utf-8')