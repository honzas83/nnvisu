import json
from typing import Any, Dict, cast
import torch

import tornado.websocket

from nnvisu.logic.model import NeuralNetwork
from nnvisu.logic.trainer import StatelessTrainer
from nnvisu.protocol import TrainingPayload

class NeuralWebSocket(tornado.websocket.WebSocketHandler): # type: ignore
    def initialize(self) -> None:
        self.trainer = StatelessTrainer()

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self) -> None:
        print("WebSocket opened")

    def on_message(self, message: str) -> None:
        try:
            data = json.loads(message)
            self.handle_message(data)
        except json.JSONDecodeError:
            print("Invalid JSON received")
        except Exception as e:
            print(f"Error handling message: {e}")
            import traceback
            traceback.print_exc()

    def handle_message(self, data: Dict[str, Any]) -> None:
        msg_type = data.get("type")

        if msg_type == "train_step":
            # Cast for type checking, though runtime dict
            payload = cast(TrainingPayload, data)
            self.handle_train_step(payload)

    def handle_train_step(self, payload: TrainingPayload) -> None:
        config = payload.get("config")
        model_state = payload.get("model")
        data_points = payload.get("data")

        if not config or not model_state or not data_points:
             # Error handling?
             return

        # Reconstruct Model
        architecture = config.get("architecture", [10, 5])
        
        # Determine required output dimension from data labels
        # Find max label in the current batch
        max_label = 0
        for p in data_points:
            lbl = p.get('label', 0)
            if lbl > max_label:
                max_label = lbl
        
        required_output_dim = max(2, max_label + 1)
        
        # Initialize model with required dimensions
        model = NeuralNetwork(hidden_layers=architecture, output_dim=required_output_dim)
        
        # Smart Load Weights
        # Iterate through layers and load weights if shapes match
        incoming_weights = cast(Dict[str, Any], model_state).get("weights", [])
        incoming_biases = cast(Dict[str, Any], model_state).get("biases", [])
        
        linear_idx = 0
        for layer in model.net:
            if isinstance(layer, torch.nn.Linear):
                if linear_idx < len(incoming_weights) and linear_idx < len(incoming_biases):
                    # Check shape compatibility
                    w_data = incoming_weights[linear_idx]
                    b_data = incoming_biases[linear_idx]
                    
                    # Incoming is list of lists, convert to tensor to check shape
                    # Optimization: Just check len(w_data) and len(w_data[0]) if possible
                    # But simpler to try/except
                    
                    try:
                        w_tensor = torch.tensor(w_data)
                        b_tensor = torch.tensor(b_data)
                        
                        if w_tensor.shape == layer.weight.shape and b_tensor.shape == layer.bias.shape:
                            layer.weight.data = w_tensor
                            layer.bias.data = b_tensor
                        else:
                            # Shape mismatch (e.g. output layer changed size)
                            # Keep initialized random weights for this layer
                            # print(f"Layer {linear_idx} shape mismatch. Keeping new initialization.")
                            pass
                    except Exception as e:
                        print(f"Error loading layer {linear_idx}: {e}")
                
                linear_idx += 1

        # Train Step
        learning_rate = config.get("learningRate", 0.01)
        try:
            loss = self.trainer.train_step(model, data_points, learning_rate)
        except IndexError as e:
            print(f"Training error: {e}")
            # Likely target out of bounds if something went wrong
            return
        
        updated_state = model.get_state_dict_as_list()
        
        # Response
        response = {
            "type": "step_result",
            "model": updated_state,
            "metrics": {
                "loss": loss,
                "accuracy": 0.0
            }
        }
        self.write_message(json.dumps(response))
        
        # Map Update
        map_b64 = self.trainer.generate_map(model)
        self.write_message(json.dumps({
            "type": "map_update",
            "payload": {
                "width": StatelessTrainer.GRID_WIDTH,
                "height": StatelessTrainer.GRID_HEIGHT,
                "format": "rgb",
                "data": map_b64
            }
        }))

    def on_close(self) -> None:
        print("WebSocket closed")
