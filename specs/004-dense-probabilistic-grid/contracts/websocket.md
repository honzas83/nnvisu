# WebSocket API Contracts

## Messages

### Server -> Client

#### Map Update
Sent after a training step to update the decision boundary visualization.

```json
{
  "type": "map_update",
  "payload": {
    "width": 100,
    "height": 100,
    "format": "rgb",
    "data": "<base64_encoded_rgb_bytes>"
  }
}
```

- **width**: 100 (Fixed resolution)
- **height**: 100 (Fixed resolution)
- **format**: "rgb" indicates 3 bytes per pixel (R, G, B).
- **data**: Base64 string of the flattened byte array. Size = 100 * 100 * 3 = 30,000 bytes (decoded).

### Client -> Server

#### Train Step
(Unchanged from baseline)

