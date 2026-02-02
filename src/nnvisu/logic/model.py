import torch
from torch import nn
from typing import Dict, Any

class NeuralNetwork(nn.Module): # type: ignore
    def __init__(self, hidden_layers: list[int] | None = None, output_dim: int = 2):
        super().__init__()
        if hidden_layers is None:
            hidden_layers = [10, 5]
        
        layers: list[nn.Module] = []
        input_dim = 2
        
        for h in hidden_layers:
            layers.append(nn.Linear(input_dim, h))
            layers.append(nn.Tanh())
            input_dim = h
            
        layers.append(nn.Linear(input_dim, output_dim)) # Output classes (logits)
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
    
    def get_state_dict_as_list(self) -> Dict[str, Any]:
        """Export weights and biases as simple lists."""
        weights = []
        biases = []
        for layer in self.net:
            if isinstance(layer, nn.Linear):
                # Convert to python lists
                weights.append(layer.weight.data.tolist())
                biases.append(layer.bias.data.tolist())
        return {"weights": weights, "biases": biases}

    def load_state_dict_from_list(self, state: Dict[str, Any]) -> None:
        """Load weights and biases from simple lists."""
        weight_list = state.get("weights", [])
        bias_list = state.get("biases", [])
        
        linear_idx = 0
        for layer in self.net:
            if isinstance(layer, nn.Linear):
                if linear_idx < len(weight_list):
                    layer.weight.data = torch.tensor(weight_list[linear_idx])
                if linear_idx < len(bias_list):
                    layer.bias.data = torch.tensor(bias_list[linear_idx])
                linear_idx += 1

