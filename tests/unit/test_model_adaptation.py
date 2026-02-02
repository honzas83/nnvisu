import torch
from nnvisu.logic.model import NeuralNetwork

def test_adapt_output_layer_add():
    # Initial model with 2 output classes
    model = NeuralNetwork(hidden_layers=[10], output_dim=2)
    original_output_layer = list(model.net.children())[-1]
    assert original_output_layer.out_features == 2
    
    # Adapt to 4 classes
    # We will implement this method in T002
    model.adapt_output_layer(4)
    
    new_output_layer = list(model.net.children())[-1]
    assert new_output_layer.out_features == 4
    assert new_output_layer.in_features == 10
    
    # Verify existing weights are preserved for the first 2 classes
    # This requires us to compare the weight values
    pass

def test_adapt_output_layer_remove():
    # Initial model with 4 output classes
    model = NeuralNetwork(hidden_layers=[10], output_dim=4)
    
    # Adapt to 2 classes
    model.adapt_output_layer(2)
    
    new_output_layer = list(model.net.children())[-1]
    assert new_output_layer.out_features == 2
    assert new_output_layer.in_features == 10
