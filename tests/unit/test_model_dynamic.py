import torch
import torch.nn as nn
from nnvisu.logic.model import NeuralNetwork

def test_default_architecture() -> None:
    """Test that default initialization works (legacy behavior)."""
    model = NeuralNetwork()
    assert len(model.net) > 0
    # Check default structure: [10, 5] hidden -> 2 output
    # Layers: Linear(2->10), Tanh, Linear(10->5), Tanh, Linear(5->2)
    assert isinstance(model.net[0], nn.Linear)
    assert model.net[0].in_features == 2
    assert model.net[0].out_features == 10
    assert model.net[-1].out_features == 2

def test_dynamic_architecture_config() -> None:
    """Test initialization with custom hidden layers."""
    hidden_layers = [8, 4, 3]
    model = NeuralNetwork(hidden_layers=hidden_layers, output_dim=2)
    
    # Check layers
    # Linear(2->8), Tanh, Linear(8->4), Tanh, Linear(4->3), Tanh, Linear(3->2)
    
    # Layer 0: Input -> H1
    assert model.net[0].in_features == 2
    assert model.net[0].out_features == 8
    
    # Layer 2: H1 -> H2
    assert model.net[2].in_features == 8
    assert model.net[2].out_features == 4
    
    # Layer 4: H2 -> H3
    assert model.net[4].in_features == 4
    assert model.net[4].out_features == 3
    
    # Layer 6: H3 -> Output
    assert model.net[6].in_features == 3
    assert model.net[6].out_features == 2

def test_custom_output_dim() -> None:
    """Test initialization with custom output dimension (for 3 classes)."""
    model = NeuralNetwork(hidden_layers=[5], output_dim=3)
    # Last layer should output 3
    assert model.net[-1].out_features == 3

def test_empty_hidden_layers() -> None:
    """Test initialization with 0 hidden layers (Linear Perceptron)."""
    model = NeuralNetwork(hidden_layers=[], output_dim=2)
    # Should be just one Linear layer: 2 -> 2
    assert len(model.net) == 1
    assert isinstance(model.net[0], nn.Linear)
    assert model.net[0].in_features == 2
    assert model.net[0].out_features == 2

def test_forward_pass_shape() -> None:
    """Test that forward pass returns correct shape."""
    model = NeuralNetwork(hidden_layers=[5], output_dim=3)
    batch_size = 4
    x = torch.randn(batch_size, 2)
    output = model(x)
    assert output.shape == (batch_size, 3)