import json
from typing import Any
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.websocket import websocket_connect
from nnvisu.app import make_app

class TestArchitectureUpdate(AsyncHTTPTestCase):
    def get_app(self) -> Any:
        return make_app()

    @gen_test
    def test_architecture_update_applies(self) -> None:
        url = self.get_url('/ws').replace('http', 'ws')
        client = yield websocket_connect(url)

        # Consume initial config message
        yield client.read_message()

        # 1. Update config with new architecture [7]
        update_msg = {
            "type": "update_config",
            "payload": { "architecture": [7] }
        }
        client.write_message(json.dumps(update_msg))

        # 2. Reset model (should use the config above if fixed, but currently uses [10, 10])
        reset_msg = { "type": "reset" }
        client.write_message(json.dumps(reset_msg))

        # 3. Add some data so training can start
        data_msg = {
            "type": "update_data",
            "data": [{"x": 0.1, "y": 0.2, "label": 0}]
        }
        client.write_message(json.dumps(data_msg))

        # 4. Start training
        start_msg = { "type": "start_training" }
        client.write_message(json.dumps(start_msg))

        # 5. Wait for step_result and check architecture
        # Note: it might take a moment to get the first result
        found_weights = False
        for _ in range(20):
            resp_str = yield client.read_message()
            if resp_str is None:
                break
            
            if isinstance(resp_str, bytes):
                continue
                
            resp = json.loads(resp_str)
            if resp.get("type") == "step_result" and resp.get("model"):
                weights = resp["model"]["weights"]
                # Weights for Linear(2 -> 7) should have 7 rows
                # Currently it's likely Linear(2 -> 10) -> 10 rows
                first_layer_weights = weights[0]
                assert len(first_layer_weights) == 7, f"Expected 7 neurons in first hidden layer, got {len(first_layer_weights)}"
                found_weights = True
                break
        
        assert found_weights, "Did not receive model weights in step_result"
        client.close()
