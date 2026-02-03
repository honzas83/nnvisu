import json
from typing import Any
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.websocket import websocket_connect
from nnvisu.app import make_app

class TestConcurrency(AsyncHTTPTestCase): # type: ignore
    def get_app(self) -> Any:
        return make_app()

    @gen_test # type: ignore
    def test_concurrent_training(self) -> None: # type: ignore
        # Create two clients
        url = self.get_url('/ws').replace('http', 'ws')
        c1 = yield websocket_connect(url)
        c2 = yield websocket_connect(url)

        # Consume initial config message
        yield c1.read_message()
        yield c2.read_message()

        # Config 1: 2->10->2
        payload1 = {
            "type": "train_step",
            "config": { "architecture": [10], "learningRate": 0.1 },
            "model": { "weights": [], "biases": [] }, # Empty means init new
            "data": [{ "x": 0.5, "y": 0.5, "label": 1 }]
        }

        # Config 2: 2->5->2
        payload2 = {
            "type": "train_step",
            "config": { "architecture": [5], "learningRate": 0.1 },
            "model": { "weights": [], "biases": [] }, 
            "data": [{ "x": -0.5, "y": -0.5, "label": 0 }]
        }

        # Send both
        c1.write_message(json.dumps(payload1))
        c2.write_message(json.dumps(payload2))

        # Wait for responses
        
        resp1_str = yield c1.read_message()
        resp2_str = yield c2.read_message()
        
        resp1 = json.loads(resp1_str)
        resp2 = json.loads(resp2_str)
        
        # Verify type
        assert resp1["type"] == "step_result"
        assert resp2["type"] == "step_result"
        
        # Verify isolation via architecture size
        # Model 1: Hidden layer 0 should have 10 units -> weight matrix [10, 2]
        # Model 2: Hidden layer 0 should have 5 units -> weight matrix [5, 2]
        
        w1 = resp1["model"]["weights"][0]
        w2 = resp2["model"]["weights"][0]

        assert len(w1) == 10
        assert len(w2) == 5

        c1.close()
        c2.close()