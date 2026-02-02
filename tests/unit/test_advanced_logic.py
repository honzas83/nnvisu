import torch
from nnvisu.logic.model import NeuralNetwork
from nnvisu.logic.trainer import StatelessTrainer

def test_neural_network_activation_switching():
    # Test Tanh
    model_tanh = NeuralNetwork(hidden_layers=[10], output_dim=2, activation='tanh')
    assert any(isinstance(m, torch.nn.Tanh) for m in model_tanh.net)
    
    # Test ReLU
    model_relu = NeuralNetwork(hidden_layers=[10], output_dim=2, activation='relu')
    assert any(isinstance(m, torch.nn.ReLU) for m in model_relu.net)
    
    # Test GELU
    model_gelu = NeuralNetwork(hidden_layers=[10], output_dim=2, activation='gelu')
    assert any(isinstance(m, torch.nn.GELU) for m in model_gelu.net)

def test_neural_network_dropout_injection():
    # Test No Dropout
    model_no_drop = NeuralNetwork(hidden_layers=[10], output_dim=2, dropout=0.0)
    assert not any(isinstance(m, torch.nn.Dropout) for m in model_no_drop.net)
    
    # Test With Dropout
    model_drop = NeuralNetwork(hidden_layers=[10], output_dim=2, dropout=0.5)
    assert any(isinstance(m, torch.nn.Dropout) for m in model_drop.net)

def test_trainer_optimizer_selection():
    trainer = StatelessTrainer()
    model = NeuralNetwork(hidden_layers=[5], output_dim=2)
    data = [{'x': 0.1, 'y': 0.2, 'label': 0}]
    
    # This is a bit tricky to test directly as optimizers are local to train_step
    # but we can verify the function runs without error for different configs
    
    config_adam = {
        'optimizer': 'adam',
        'learningRate': 0.01,
        'regularization': 0.0,
        'batchSize': 0
    }
    loss_adam = trainer.train_step(model, data, config_adam)
    assert isinstance(loss_adam, float)
    
    config_sgd = {
        'optimizer': 'sgd',
        'learningRate': 0.01,
        'regularization': 0.01,
        'batchSize': 0
    }
    loss_sgd = trainer.train_step(model, data, config_sgd)
    assert isinstance(loss_sgd, float)

def test_trainer_batch_sampling():
    trainer = StatelessTrainer()
    model = NeuralNetwork(hidden_layers=[5], output_dim=2)
    data = [
        {'x': 0.1, 'y': 0.1, 'label': 0},
        {'x': 0.2, 'y': 0.2, 'label': 1},
        {'x': 0.3, 'y': 0.3, 'label': 0},
        {'x': 0.4, 'y': 0.4, 'label': 1},
    ]
    
    config_batch = {
        'optimizer': 'adam',
        'learningRate': 0.01,
        'regularization': 0.0,
        'batchSize': 2
    }
    
    # Again, verifying it runs. 
    # Sampling logic happens inside train_step.
    loss = trainer.train_step(model, data, config_batch)
    assert isinstance(loss, float)
