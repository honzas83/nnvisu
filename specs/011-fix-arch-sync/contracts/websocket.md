# WebSocket Contract: Architecture Updates

## Outgoing (Client -> Server)

### update_architecture
Sent by the client whenever the network structure is modified in the UI.

```json
{
  "type": "update_architecture",
  "payload": {
    "hidden_layers": [10, 8, 4],
    "activation": "relu",
    "dropout": 0.1
  }
}
```

**Constraints**:
- `hidden_layers` length: 0 to 10.
- Each element in `hidden_layers`: 1 to 100.
- `activation`: One of `["tanh", "relu", "leaky_relu", "gelu"]`.

## Incoming (Server -> Client)

### architecture_synced
Sent by the server after the backend model has been successfully rebuilt and re-initialized.

```json
{
  "type": "architecture_synced",
  "payload": {
    "status": "success",
    "hidden_layers": [10, 8, 4]
  }
}
```
