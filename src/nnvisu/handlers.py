import json
from typing import Any, Dict, cast

import tornado.websocket

from nnvisu.logic.model import NeuralNetwork
from nnvisu.logic.trainer import StatelessTrainer
from nnvisu.protocol import TrainingPayload, GenerateDataRequest
from nnvisu.logic.generators import (
    generate_circles, generate_moons, generate_blobs,
    generate_anisotropic, generate_varied_variance
)

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
        elif msg_type == "generate_data":
            payload = cast(GenerateDataRequest, data)
            self.handle_generate_data(payload)

    def handle_generate_data(self, payload: GenerateDataRequest) -> None:
        dist_type = payload.get("distribution")
        num_classes = payload.get("num_classes", 2)
        
        try:
            if dist_type == "circles":
                data = generate_circles(n_classes=num_classes)
            elif dist_type == "moons":
                data = generate_moons(n_classes=num_classes)
            elif dist_type == "blobs":
                data = generate_blobs(n_classes=num_classes)
            elif dist_type == "anisotropic":
                data = generate_anisotropic(n_classes=num_classes)
            elif dist_type == "varied_variance":
                data = generate_varied_variance(n_classes=num_classes)
            else:
                self.write_message(json.dumps({
                    "type": "error",
                    "message": f"Unknown distribution type: {dist_type}"
                }))
                return
            
            self.write_message(json.dumps({
                "type": "data_generated",
                "data": data
            }))
        except Exception as e:
            self.write_message(json.dumps({
                "type": "error",
                "message": f"Error generating data: {str(e)}"
            }))

    def handle_train_step(self, payload: TrainingPayload) -> None:
        config = payload.get("config")
        model_state = payload.get("model")
        data_points = payload.get("data")

        if not config or not model_state or not data_points:
             # Error handling?
             return

        # Reconstruct Model
        architecture = config.get("architecture", [10, 5])
        activation = config.get("activation", "tanh")
        dropout = config.get("dropout", 0.0)
        
        incoming_weights = cast(Dict[str, Any], model_state).get("weights", [])
        
        # Detect old output dim from last layer weights if available
        old_output_dim = 2
        if incoming_weights:
            old_output_dim = len(incoming_weights[-1])
            
        # Initialize model with OLD dimensions first to load weights correctly
        model = NeuralNetwork(
            hidden_layers=architecture, 
            output_dim=old_output_dim,
            activation=activation,
            dropout=dropout
        )
        model.load_state_dict_from_list(cast(Dict[str, Any], model_state))

        # Determine required output dimension from data labels
        # Find max label in the current batch
        max_label = 0
        for p in data_points:
            lbl = p.get('label', 0)
            if lbl > max_label:
                max_label = lbl
        
        required_output_dim = max(2, max_label + 1)
        
        # Adapt model to new dimensions if necessary
        model.adapt_output_layer(required_output_dim)

        # Train Step
        try:
            loss = self.trainer.train_step(model, data_points, config)
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
