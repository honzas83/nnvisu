import base64
import time
import logging
import queue
from typing import List, TYPE_CHECKING

import numpy as np
import torch
from torch import nn, optim

from nnvisu.logic.model import NeuralNetwork
from nnvisu.protocol import DataPoint

if TYPE_CHECKING:
    from nnvisu.logic.session import TrainingSession

logger = logging.getLogger(__name__)

class StatelessTrainer:
    GRID_WIDTH = 100
    GRID_HEIGHT = 100

    # Class colors matching frontend (RGB)
    CLASS_COLORS = [
        [52, 152, 219],  # #3498db Blue
        [230, 126, 34], # #e67e22 Orange
        [231, 76, 60],  # #e74c3c Red
        [155, 89, 182], # #9b59b6 Purple
        [46, 204, 113], # #2ecc71 Green
        [241, 196, 15], # #f1c40f Yellow
        [121, 85, 72],  # #795548 Brown
        [52, 73, 94]    # #34495e Navy
    ]

    def __init__(self) -> None:
        self.criterion = nn.CrossEntropyLoss()

    def train_step(self, model: NeuralNetwork, data: List[DataPoint], config: dict) -> float:
        """
        Perform a single training step.
        Note: Optimizer state is not preserved between steps in this stateless design.
        """
        if not data:
            return 0.0

        # Hyperparameters from config
        learning_rate = config.get("learningRate", 0.001)
        optimizer_name = config.get("optimizer", "adam").lower()
        regularization = config.get("regularization", 0.0)
        batch_size = config.get("batchSize", 0)

        # Batch sampling
        if batch_size > 0 and batch_size < len(data):
            indices = np.random.choice(len(data), batch_size, replace=False)
            batch = [data[i] for i in indices]
        else:
            batch = data

        # Prepare batch tensors
        device = torch.device("cpu")
        X = torch.tensor([[p['x'], p['y']] for p in batch], dtype=torch.float32, device=device)  # noqa: N806
        y = torch.tensor([p['label'] for p in batch], dtype=torch.long, device=device)

        # Re-initialize optimizer (stateless)
        opt_class = {
            'sgd': optim.SGD,
            'adam': optim.Adam,
            'rmsprop': optim.RMSprop
        }.get(optimizer_name, optim.Adam)

        optimizer = opt_class(model.parameters(), lr=learning_rate, weight_decay=regularization)

        model.train() # Set to train mode for dropout
        optimizer.zero_grad()
        outputs = model(X)
        loss = self.criterion(outputs, y)
        loss.backward()
        optimizer.step()

        return float(loss.item())
        
    def generate_map(self, model: NeuralNetwork, width: int | None = None, height: int | None = None) -> str:
        """Generate classification map as base64 string (RGB bytes)."""
        w = width or self.GRID_WIDTH
        h = height or self.GRID_HEIGHT
        rgb_bytes = self.generate_binary_map(model, w, h)
        return base64.b64encode(rgb_bytes).decode('utf-8')

    def generate_binary_map(self, model: NeuralNetwork, width: int | None = None, height: int | None = None) -> bytes:
        """Generate classification map as raw RGB bytes."""
        w = width or self.GRID_WIDTH
        h = height or self.GRID_HEIGHT
        
        # Create grid
        # x: -1 to 1, y: -1 to 1
        x = np.linspace(-1, 1, w)
        y = np.linspace(1, -1, h) # Top-down for image
        xv, yv = np.meshgrid(x, y)

        # Flatten and convert to tensor
        device = torch.device("cpu")
        grid_points = np.stack([xv.flatten(), yv.flatten()], axis=1)
        X_grid = torch.tensor(grid_points, dtype=torch.float32, device=device)  # noqa: N806

        # Predict probabilities
        with torch.no_grad():
            outputs = model(X_grid)
            # Apply softmax to get posterior probabilities
            probs = torch.softmax(outputs, dim=1) # [N, num_classes]

        num_classes = probs.shape[1]
        
        # Prepare color matrix [num_classes, 3]
        colors = np.array(self.CLASS_COLORS)
        if num_classes > len(colors):
            extra = np.random.randint(0, 255, size=(num_classes - len(colors), 3))
            colors = np.vstack([colors, extra])
        else:
            colors = colors[:num_classes]

        # Calculate weighted average of colors
        blended_colors = probs.numpy() @ colors
        
        # Convert to bytes
        rgb_bytes = blended_colors.astype(np.uint8)
        return rgb_bytes.tobytes()

class StatefulTrainer(StatelessTrainer):
    """
    Stateful trainer that maintains optimizer state and runs in a loop.
    """
    def __init__(self) -> None:
        super().__init__()
        self.optimizer: optim.Optimizer | None = None
        self.current_model_id: int | None = None
        self.current_opt_name: str = ""
        self.current_lr: float = 0.0
        self.current_reg: float = 0.0

    def _get_optimizer(self, model: NeuralNetwork, config: dict) -> optim.Optimizer:
        learning_rate = config.get("learningRate", 0.001)
        optimizer_name = config.get("optimizer", "adam").lower()
        regularization = config.get("regularization", 0.0)
        model_id = id(model)

        # Check if we need to re-initialize (including if the model instance changed)
        if (self.optimizer is None or 
            model_id != self.current_model_id or
            optimizer_name != self.current_opt_name or 
            learning_rate != self.current_lr or
            regularization != self.current_reg):
            
            opt_class = {
                'sgd': optim.SGD,
                'adam': optim.Adam,
                'rmsprop': optim.RMSprop
            }.get(optimizer_name, optim.Adam)
            
            self.optimizer = opt_class(model.parameters(), lr=learning_rate, weight_decay=regularization)
            self.current_model_id = model_id
            self.current_opt_name = optimizer_name
            self.current_lr = learning_rate
            self.current_reg = regularization
            
        return self.optimizer

    def train_step_stateful(self, model: NeuralNetwork, data: List[DataPoint], config: dict) -> float:
        if not data:
            return 0.0

        batch_size = config.get("batchSize", 0)

        # Batch sampling
        if batch_size > 0 and batch_size < len(data):
            indices = np.random.choice(len(data), batch_size, replace=False)
            batch = [data[i] for i in indices]
        else:
            batch = data

        device = torch.device("cpu")
        X = torch.tensor([[p['x'], p['y']] for p in batch], dtype=torch.float32, device=device)  # noqa: N806
        y = torch.tensor([p['label'] for p in batch], dtype=torch.long, device=device)

        optimizer = self._get_optimizer(model, config)

        model.train() 
        optimizer.zero_grad()
        outputs = model(X)
        loss = self.criterion(outputs, y)
        loss.backward()
        optimizer.step()

        return float(loss.item())

    def run_loop(self, session: "TrainingSession") -> None:
        """
        The main loop to be run in a thread.
        """
        step_counter = 0
        last_log_time = time.time()

        while not session.stop_event.is_set():
            # Use lock to ensure model reference and mode (train/eval) are stable
            with session.lock:
                model, data, config = session.model, session.data, session.config.copy()
                
                if model and data:
                    try:
                        loss = self.train_step_stateful(model, data, config)
                        step_counter += 1
                        
                        # Push result to queue if not full
                        try:
                            session.step_queue.put({
                                "loss": loss,
                                "timestamp": time.time()
                            }, block=False)
                        except queue.Full:
                            pass
                            
                    except Exception as e:
                        logger.error(f"Error in training loop: {e}", exc_info=True)
            
            # Periodic logging
            now = time.time()
            if now - last_log_time >= 5.0:
                elapsed = now - last_log_time
                tps = step_counter / elapsed
                logger.info(f"[Training] Steps per second: {tps:.2f}")
                step_counter = 0
                last_log_time = now

            # Cooperative multitasking: allow main thread to run PeriodicCallback
            if not data:
                time.sleep(0.1)
            else:
                time.sleep(0.0001)