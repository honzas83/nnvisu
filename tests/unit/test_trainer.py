import base64
from nnvisu.logic.trainer import StatelessTrainer
from nnvisu.logic.model import NeuralNetwork

class TestTrainer:
    def test_generate_map_dimensions(self) -> None:
        """Verify the generated map has correct dimensions and format (RGB)."""
        trainer = StatelessTrainer()
        model = NeuralNetwork(hidden_layers=[5], output_dim=3)
        
        # Default generation is now 100x100
        b64_data = trainer.generate_map(model)
        
        binary_data = base64.b64decode(b64_data)
        # New format is RGB (3 bytes per pixel)
        expected_size = 100 * 100 * 3
        
        assert len(binary_data) == expected_size
        
    def test_generate_map_custom_dimensions(self) -> None:
        """Verify custom dimensions work with RGB format."""
        trainer = StatelessTrainer()
        model = NeuralNetwork(hidden_layers=[5], output_dim=3)
        
        b64_data = trainer.generate_map(model, width=50, height=50)
        binary_data = base64.b64decode(b64_data)
        
        expected_size = 50 * 50 * 3
        assert len(binary_data) == expected_size
