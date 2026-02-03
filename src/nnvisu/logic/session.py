import threading
import uuid
import queue
import copy
from typing import List, Dict, Any, Optional

from nnvisu.logic.model import NeuralNetwork
from nnvisu.protocol import DataPoint

class TrainingSession:
    """
    Manages the state of a single training session, including the model, data,
    configuration, and thread synchronization.
    """
    def __init__(self) -> None:
        self.id: str = str(uuid.uuid4())
        self.model: Optional[NeuralNetwork] = None
        self.data: List[DataPoint] = []
        self.config: Dict[str, Any] = {}
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Communication with main thread
        # We use a queue size of 1 to ensure we only send the latest update
        # However, for metric updates we might want a simple queue.
        # For the map generation, we probably want to skip if full.
        self.step_queue: queue.Queue = queue.Queue() # For metrics
        self.map_queue: queue.Queue = queue.Queue() # For map binary data
        
        # Control flags
        self.training_active = False
        self.stop_event = threading.Event()
        self.training_thread: Optional[threading.Thread] = None

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Thread-safe configuration update."""
        with self.lock:
            self.config.update(new_config)

    def set_data(self, data: List[DataPoint]) -> None:
        """Thread-safe data update."""
        with self.lock:
            self.data = data

    def set_model(self, model: NeuralNetwork) -> None:
        """Thread-safe model update."""
        with self.lock:
            self.model = model

    def get_snapshot(self) -> tuple[Optional[NeuralNetwork], List[DataPoint], Dict[str, Any]]:
        """
        Get a snapshot of the current state (model, data, config) for training.
        Note: We return references. The visualization thread should be careful.
        """
        with self.lock:
            return self.model, self.data, self.config.copy()

    def reset_steps(self) -> None:
        """Clear the step queue and reset any internal counters."""
        with self.step_queue.mutex:
            self.step_queue.queue.clear()
        with self.map_queue.mutex:
            self.map_queue.queue.clear()
