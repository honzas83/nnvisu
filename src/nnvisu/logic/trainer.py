import base64
from typing import List

import numpy as np
import torch
from torch import nn, optim

from nnvisu.logic.model import NeuralNetwork
from nnvisu.protocol import DataPoint

class StatelessTrainer:
    def __init__(self) -> None:
        self.criterion = nn.CrossEntropyLoss()

    def train_step(self, model: NeuralNetwork, data: List[DataPoint], learning_rate: float) -> float:
        """
        Perform a single training step.
        Note: Optimizer state is not preserved between steps in this stateless design.
        """
        if not data:
            return 0.0

        # Prepare batch
        X = torch.tensor([[p['x'], p['y']] for p in data], dtype=torch.float32)  # noqa: N806
        y = torch.tensor([p['label'] for p in data], dtype=torch.long)

        # Re-initialize optimizer (stateless)
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        optimizer.zero_grad()
        outputs = model(X)
        loss = self.criterion(outputs, y)
        loss.backward()
        optimizer.step()

        return float(loss.item())

    def generate_map(self, model: NeuralNetwork, width: int = 50, height: int = 50) -> str:
        """Generate classification map as base64 string."""
        # Create grid
        # x: -1 to 1, y: -1 to 1
        x = np.linspace(-1, 1, width)
        y = np.linspace(1, -1, height) # Top-down for image
        xv, yv = np.meshgrid(x, y)

        # Flatten and convert to tensor
        grid_points = np.stack([xv.flatten(), yv.flatten()], axis=1)
        X_grid = torch.tensor(grid_points, dtype=torch.float32)  # noqa: N806

        # Predict
        with torch.no_grad():
            outputs = model(X_grid)
            _, predicted = torch.max(outputs, 1)

        # Convert to bytes
        class_ids = predicted.numpy().astype(np.uint8)
        return base64.b64encode(class_ids.tobytes()).decode('utf-8')