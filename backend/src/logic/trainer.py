import base64

import numpy as np
import torch
from torch import nn, optim

from logic.model import NeuralNetwork, TrainingState


class Trainer:
    def __init__(self, state: TrainingState):
        self.state = state
        self.criterion = nn.CrossEntropyLoss()

    def initialize_model(self, learning_rate: float = 0.01) -> None:
        # Determine output dimension based on data
        num_classes = 2
        if self.state.points:
            max_label = max(p.label for p in self.state.points)
            num_classes = max(2, max_label + 1)
        
        # If model exists but output dim mismatches, or model doesn't exist, re-init
        if self.state.model is None or self.state.output_dim != num_classes:
            self.state.output_dim = num_classes
            self.state.model = NeuralNetwork(
                hidden_layers=self.state.hidden_layers,
                output_dim=self.state.output_dim
            )
            # New optimizer for new parameters
            self.state.optimizer = optim.Adam(self.state.model.parameters(), lr=learning_rate)
            self.state.epoch = 0
        elif self.state.optimizer is None:
             # Just ensure optimizer exists if model was kept
             self.state.optimizer = optim.Adam(self.state.model.parameters(), lr=learning_rate)

    def step(self) -> float:
        if not self.state.points or self.state.model is None:
            return 0.0

        # Prepare batch
        X = torch.tensor([[p.x, p.y] for p in self.state.points], dtype=torch.float32)  # noqa: N806
        y = torch.tensor([p.label for p in self.state.points], dtype=torch.long)

        self.state.optimizer.zero_grad()
        outputs = self.state.model(X)
        loss = self.criterion(outputs, y)
        loss.backward()
        self.state.optimizer.step()

        loss_val = float(loss.item())
        self.state.loss = loss_val
        self.state.epoch += 1
        return loss_val

    def generate_map(self, width: int = 50, height: int = 50) -> str:
        if self.state.model is None:
            return ""

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
            outputs = self.state.model(X_grid)
            _, predicted = torch.max(outputs, 1)

        # Convert to bytes
        class_ids = predicted.numpy().astype(np.uint8)
        return base64.b64encode(class_ids.tobytes()).decode('utf-8')
