import asyncio
import json
from typing import Any

import tornado.ioloop
import tornado.websocket

import protocol
from logic.model import TrainingState
from logic.trainer import Trainer

# Global set of connected clients for broadcasting
clients: set['NeuralWebSocket'] = set()
training_task: asyncio.Task | None = None

class NeuralWebSocket(tornado.websocket.WebSocketHandler):
    def initialize(self, state: TrainingState) -> None:
        self.state = state
        self.trainer = Trainer(state)

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self) -> None:
        print("WebSocket opened")
        clients.add(self)
        # Send existing points
        for point in self.state.points:
            self.write_message(json.dumps({
                "type": protocol.MSG_ADD_POINT,
                "payload": {
                    "id": point.id,
                    "x": point.x,
                    "y": point.y,
                    "label": point.label
                }
            }))
        # Send current status
        self.write_message(json.dumps({
            "type": protocol.MSG_TRAINING_STATUS,
            "payload": {
                "is_training": self.state.is_training,
                "epoch": self.state.epoch,
                "loss": self.state.loss
            }
        }))

    def on_message(self, message: str) -> None:
        try:
            data = json.loads(message)
            self.handle_message(data)
        except json.JSONDecodeError:
            print("Invalid JSON received")

    def handle_message(self, data: dict[str, Any]) -> None:
        msg_type = data.get("type")
        payload = data.get("payload", {})

        if msg_type == protocol.MSG_ADD_POINT:
            point = self.state.add_point(
                x=payload.get("x", 0.0),
                y=payload.get("y", 0.0),
                label=payload.get("label", 0)
            )
            self.broadcast(json.dumps({
                "type": protocol.MSG_ADD_POINT,
                "payload": {
                    "id": point.id,
                    "x": point.x,
                    "y": point.y,
                    "label": point.label
                }
            }))

        elif msg_type == protocol.MSG_CLEAR_POINTS:
            self.state.clear_points()
            self.broadcast(json.dumps({"type": protocol.MSG_CLEAR_POINTS}))

        elif msg_type == protocol.MSG_START_TRAINING:
            if not self.state.is_training:
                self.state.is_training = True
                self.trainer.initialize_model(learning_rate=payload.get("learning_rate", 0.01))
                global training_task  # noqa: PLW0603
                if training_task is None or training_task.done():
                    training_task = asyncio.create_task(self.run_training_loop())

        elif msg_type == protocol.MSG_STOP_TRAINING:
            self.state.is_training = False

        elif msg_type == protocol.MSG_RESET_MODEL:
            self.state.is_training = False
            self.state.model = None # Force re-init
            self.state.optimizer = None
            self.state.epoch = 0
            self.state.loss = 0.0
            # Broadcast status reset
            self.broadcast(json.dumps({
                "type": protocol.MSG_TRAINING_STATUS,
                "payload": {
                    "is_training": False,
                    "epoch": 0,
                    "loss": 0.0
                }
            }))
            # Clear map
            # Optional: Broadcast empty/clear map


    async def run_training_loop(self) -> None:
        print("Training started")
        while self.state.is_training:
            loss = self.trainer.step()

            # Broadcast status (every step? maybe throttle)
            status_msg = json.dumps({
                "type": protocol.MSG_TRAINING_STATUS,
                "payload": {
                    "is_training": True,
                    "epoch": self.state.epoch,
                    "loss": loss
                }
            })
            self.broadcast(status_msg)

            # Broadcast Map (throttle: every 10 epochs or 100ms)
            if self.state.epoch % 10 == 0:
                map_b64 = self.trainer.generate_map(width=50, height=50)
                map_msg = json.dumps({
                    "type": protocol.MSG_MAP_UPDATE,
                    "payload": {
                        "width": 50,
                        "height": 50,
                        "data": map_b64
                    }
                })
                self.broadcast(map_msg)

            await asyncio.sleep(0.01) # Yield to event loop

        print("Training stopped")
        # Final status update
        self.broadcast(json.dumps({
            "type": protocol.MSG_TRAINING_STATUS,
            "payload": {
                "is_training": False,
                "epoch": self.state.epoch,
                "loss": self.state.loss
            }
        }))

    def broadcast(self, msg: str) -> None:
        for client in clients:
            try:
                client.write_message(msg)
            except Exception:
                pass # Client disconnected

    def on_close(self) -> None:
        print("WebSocket closed")
        clients.remove(self)

