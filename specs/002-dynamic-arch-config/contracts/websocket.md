# Websocket API Contract

**Status**: Proposed Update
**Based on**: `specs/001-nn-training-viz/contracts/websocket.md`

## Client -> Server Messages

### `RESET_MODEL`
Resets the model weights and updates the architecture.

```json
{
  "type": "RESET_MODEL",
  "payload": {
    "hidden_layers": [10, 5] 
  }
}
```
*   `payload.hidden_layers`: (Optional) List of integers defining hidden layer sizes. If omitted, uses default.

### `ADD_POINT`
Adds a training point.

```json
{
  "type": "ADD_POINT",
  "payload": {
    "x": 0.5,
    "y": -0.2,
    "label": 2
  }
}
```
*   `label`: Now supports `2` (Red class).

## Server -> Client Messages

### `MAP_UPDATE`
Sends the decision boundary map.

```json
{
  "type": "MAP_UPDATE",
  "payload": {
    "width": 50,
    "height": 50,
    "data": "<base64_encoded_uint8_array>" 
  }
}
```
*   `data`: Byte array where values can be `0`, `1`, or `2`.
