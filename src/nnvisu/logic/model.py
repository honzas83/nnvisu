import torch
from torch import nn
from typing import Dict, Any

class NeuralNetwork(nn.Module): # type: ignore
    def __init__(
        self, 
        hidden_layers: list[int] | None = None, 
        output_dim: int = 2,
        activation: str = 'tanh',
        dropout: float = 0.0
    ):
        super().__init__()
        if hidden_layers is None:
            hidden_layers = [10, 5]
        
        layers: list[nn.Module] = []
        input_dim = 2
        
        # Activation mapping
        act_fn = {
            'tanh': nn.Tanh,
            'relu': nn.ReLU,
            'leaky_relu': lambda: nn.LeakyReLU(0.01),
            'gelu': nn.GELU
        }.get(activation.lower(), nn.Tanh)

        for h in hidden_layers:
            layers.append(nn.Linear(input_dim, h))
            layers.append(act_fn())
            if dropout > 0:
                layers.append(nn.Dropout(p=dropout))
            input_dim = h
            
        layers.append(nn.Linear(input_dim, output_dim)) # Output classes (logits)
        self.net = nn.Sequential(*layers)
        self.to(torch.device("cpu"))

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
        
        device = torch.device("cpu")
        linear_idx = 0
        for layer in self.net:
            if isinstance(layer, nn.Linear):
                if linear_idx < len(weight_list):
                    layer.weight.data = torch.tensor(weight_list[linear_idx], device=device)
                if linear_idx < len(bias_list):
                    layer.bias.data = torch.tensor(bias_list[linear_idx], device=device)
                linear_idx += 1

    def adapt_output_layer(self, new_output_dim: int) -> None:
        """Adapt the final layer to a new number of output classes."""
        last_layer_idx = len(self.net) - 1
        old_layer = self.net[last_layer_idx]
        assert isinstance(old_layer, nn.Linear)
        
        old_output_dim = old_layer.out_features
        if old_output_dim == new_output_dim:
            return
            
        device = torch.device("cpu")
        in_features = old_layer.in_features
        new_layer = nn.Linear(in_features, new_output_dim).to(device)
        
        # Copy existing weights/biases
        with torch.no_grad():
            min_out = min(old_output_dim, new_output_dim)
            new_layer.weight[:min_out] = old_layer.weight[:min_out]
            new_layer.bias[:min_out] = old_layer.bias[:min_out]
            
            # If adding classes, new ones are already randomized by nn.Linear init
            
        self.net[last_layer_idx] = new_layer

