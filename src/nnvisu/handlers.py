import json
import threading
import time
from typing import Any, Dict, cast, List

import tornado.websocket
import tornado.ioloop

from nnvisu import __version__, __author__
from nnvisu.logic.model import NeuralNetwork
from nnvisu.logic.trainer import StatelessTrainer, StatefulTrainer
from nnvisu.logic.session import TrainingSession
from nnvisu.protocol import GenerateDataRequest, DataPoint, TrainingPayload
from nnvisu.logic.generators import (
    generate_circles, generate_moons, generate_blobs,
    generate_anisotropic, generate_varied_variance
)

class NeuralWebSocket(tornado.websocket.WebSocketHandler): # type: ignore
    def initialize(self) -> None:
        self.session = TrainingSession()
        self.trainer = StatefulTrainer()
        # Periodic callback for checking updates from the training thread
        self.callback = tornado.ioloop.PeriodicCallback(self.check_training_updates, 33) # ~30 FPS
        self.total_steps = 0
        self.last_model_update_time = 0

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self) -> None:
        print("WebSocket opened")
        # Start the update checker
        self.callback.start()
        
        # Send initial configuration and metadata
        self.write_message(json.dumps({
            "type": "config",
            "payload": {
                "version": __version__,
                "author": __author__
            }
        }))

    def check_training_updates(self) -> None:
        # Check for metric updates
        try:
            latest_metric = None
            drained_count = 0
            
            # Drain queue to get latest
            while not self.session.step_queue.empty():
                try:
                    latest_metric = self.session.step_queue.get_nowait()
                    drained_count += 1
                except:
                    break
            
            if latest_metric:
                self.total_steps += drained_count
                
                # Use session lock to safely access model for visualization
                with self.session.lock:
                    model = self.session.model
                    if model:
                        # Throttle sending full model weights (JSON is heavy)
                        now = time.time()
                        model_state = None
                        if now - self.last_model_update_time > 1.0: # Once per second
                            model_state = model.get_state_dict_as_list()
                            self.last_model_update_time = now

                        # 1. Send Metrics
                        self.write_message(json.dumps({
                            "type": "step_result",
                            "model": model_state,
                            "metrics": {
                                "loss": latest_metric["loss"],
                                "step": self.total_steps
                            }
                        }))
                        
                        # 2. Generate and send binary map (Fast)
                        width = StatelessTrainer.GRID_WIDTH
                        height = StatelessTrainer.GRID_HEIGHT
                        rgb_bytes = self.trainer.generate_binary_map(model, width, height)
                        
                        header = bytearray()
                        header.append(0x01) # TYPE: Map Update
                        header.extend(width.to_bytes(2, 'little'))
                        header.extend(height.to_bytes(2, 'little'))
                        
                        payload = header + rgb_bytes
                        self.write_message(bytes(payload), binary=True)
                    
        except Exception as e:
            print(f"Update handler error: {e}")
            pass

    def on_message(self, message: str) -> None:
        try:
            # Handle binary messages? For now mostly JSON.
            if isinstance(message, str):
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
        print(f"Received message: {msg_type}")

        if msg_type == "start_training":
            self.handle_start_training()
        elif msg_type == "stop_training":
            self.handle_stop_training()
        elif msg_type == "reset":
            print("Processing reset command...")
            self.handle_reset()
            print("Reset command processed.")
        elif msg_type == "update_config":
            self.handle_update_config(data)
        elif msg_type == "generate_data":
            payload = cast(GenerateDataRequest, data)
            self.handle_generate_data(payload)
        elif msg_type == "train_step":
             # Legacy support or allow client to drive stepping manually?
             # For now, ignore or implement as single step.
             payload = cast(TrainingPayload, data)
             self.handle_train_step(payload)
        elif msg_type == "update_data":
             # Implicit support for data updates
             self.handle_update_data(data)

    def handle_reset(self) -> None:
        was_active = self.session.training_active
        print(f"handle_reset: was_active={was_active}")
        
        # Always stop training if it was active
        if was_active:
            print("handle_reset: stopping training")
            self.handle_stop_training()
        
        self.total_steps = 0
        self.session.reset_steps()
        
        print("handle_reset: resetting steps and model")
        # Initialize default model
        self._init_default_model()
        
        # Critical: Adapt the new model to existing data to prevent dimension mismatch
        with self.session.lock:
            existing_data = self.session.data
            if existing_data and self.session.model:
                max_label = 0
                for p in existing_data:
                    lbl = p.get('label', 0)
                    if lbl > max_label:
                        max_label = lbl
                required_dim = max(2, max_label + 1)
                self.session.model.adapt_output_layer(required_dim)
        
        print("handle_reset: reset complete (training stopped)")

    def handle_train_step(self, payload: TrainingPayload) -> None:
        config = payload.get("config")
        model_state = payload.get("model")
        data_points = payload.get("data")

        if not config or not model_state or not data_points:
             return

        # Reconstruct Model logic similar to old implementation
        # But here we update the session model
        architecture = config.get("architecture", [10, 5])
        activation = config.get("activation", "tanh")
        dropout = config.get("dropout", 0.0)
        
        # We need to load state from payload into session model
        # Create temp model to load state
        # Detect old output dim
        incoming_weights = cast(Dict[str, Any], model_state).get("weights", [])
        old_output_dim = 2
        if incoming_weights:
            old_output_dim = len(incoming_weights[-1])

        # Safely update session
        with self.session.lock:
             # Create new model if needed or update existing
             # Since payload has state, we should probably use it.
             # But session model might be newer? 
             # For legacy test, we assume payload is authoritative.
             
             model = NeuralNetwork(
                hidden_layers=architecture, 
                output_dim=old_output_dim,
                activation=activation,
                dropout=dropout
             )
             model.load_state_dict_from_list(cast(Dict[str, Any], model_state))
             
             # Adapt
             max_label = 0
             for p in data_points:
                lbl = p.get('label', 0)
                if lbl > max_label:
                    max_label = lbl
            
             required_output_dim = max(2, max_label + 1)
             model.adapt_output_layer(required_output_dim)
             
             self.session.set_model(model)
             self.session.set_data(data_points)
             self.session.update_config(config)
             
             # Run one step
             # We use the trainer on the main thread (blocking for a bit)
             loss = self.trainer.train_step_stateful(model, data_points, config)
             
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

    def handle_update_data(self, data: Dict[str, Any]) -> None:
        points = data.get("data", [])
        if points:
            # Atomic update of data and model adaptation to prevent race conditions
            self._update_data_and_adapt_model(points)

    def _update_data_and_adapt_model(self, data: List[DataPoint]) -> None:
        # Determine required output dimension from data labels
        max_label = 0
        for p in data:
            lbl = p.get('label', 0)
            if lbl > max_label:
                max_label = lbl
        
        required_output_dim = max(2, max_label + 1)
        
        # Safely pause training if active
        was_active = self.session.training_active
        if was_active:
            self.handle_stop_training()

        with self.session.lock:
            # Update data while locked
            self.session.data = data
            
            if not self.session.model:
                self._init_default_model()
            
            if self.session.model:
                 self.session.model.adapt_output_layer(required_output_dim)
                 
        if was_active:
            self.handle_start_training()

    def handle_start_training(self) -> None:
        if self.session.training_active:
            return

        # Ensure model exists
        if not self.session.model:
            # Initialize default model
            self._init_default_model()

        self.session.stop_event.clear()
        self.session.training_active = True
        
        # Spawn thread
        t = threading.Thread(target=self.trainer.run_loop, args=(self.session,))
        t.daemon = True
        t.start()
        self.session.training_thread = t

    def handle_stop_training(self) -> None:
        if not self.session.training_active:
            return
            
        self.session.stop_event.set()
        if self.session.training_thread:
            self.session.training_thread.join(timeout=1.0)
            
        self.session.training_active = False
        self.session.training_thread = None

    def handle_update_config(self, data: Dict[str, Any]) -> None:
        payload = data.get("payload", {})
        config = payload if payload else data.get("config", {})
        self.session.update_config(config)

    def handle_generate_data(self, payload: GenerateDataRequest) -> None:
        dist_type = payload.get("distribution")
        num_classes = payload.get("num_classes", 2)
        
        try:
            data: List[DataPoint] = []
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
            
            self._update_data_and_adapt_model(data)
            
            self.write_message(json.dumps({
                "type": "data_generated",
                "data": data
            }))
        except Exception as e:
            self.write_message(json.dumps({
                "type": "error",
                "message": f"Error generating data: {str(e)}"
            }))

    def _init_default_model(self) -> None:
        model = NeuralNetwork(hidden_layers=[10, 10], output_dim=2)
        self.session.set_model(model)

    def on_close(self) -> None:
        print("WebSocket closed")
        self.handle_stop_training()
        self.callback.stop()