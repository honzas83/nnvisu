import uuid
from dataclasses import dataclass

import torch
from torch import nn


@dataclass
class TrainingExample:
    id: str
    x: float
    y: float
    label: int

    @staticmethod
    def create(x: float, y: float, label: int) -> "TrainingExample":
        return TrainingExample(id=str(uuid.uuid4()), x=x, y=y, label=label)

class NeuralNetwork(nn.Module):
    def __init__(self, hidden_layers: list[int] | None = None):
        super().__init__()
        if hidden_layers is None:
            hidden_layers = [10, 5]
        layers = []
        input_dim = 2
        for h in hidden_layers:
            layers.append(nn.Linear(input_dim, h))
            layers.append(nn.Tanh())
            input_dim = h
        layers.append(nn.Linear(input_dim, 2)) # Output 2 classes (logits)
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

@dataclass
class TrainingState:
    points: list[TrainingExample]
    model: NeuralNetwork | None = None
    optimizer: torch.optim.Optimizer | None = None
    is_training: bool = False
    epoch: int = 0
    loss: float = 0.0

    def add_point(self, x: float, y: float, label: int) -> TrainingExample:
        point = TrainingExample.create(x, y, label)
        self.points.append(point)
        return point

    def clear_points(self) -> None:
        self.points.clear()
        self.epoch = 0
        self.loss = 0.0
        self.is_training = False
        self.model = None # Reset model when points cleared? Or keep? Usually clear.

