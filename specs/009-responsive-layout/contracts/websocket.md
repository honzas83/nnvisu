# WebSocket Contract: Proxy-Aware Connection

## Connection Handshake

### URL Resolution (Frontend)
The client must dynamically resolve the WebSocket endpoint to support hosting on subpaths and behind SSL-terminating proxies.

**Algorithm**:
1. Determine `base_protocol`: `wss:` if `location.protocol` is `https:`, else `ws:`.
2. Determine `app_path`: `location.pathname` stripped of trailing slash.
3. Construct `ws_url`: `${base_protocol}//${location.host}${app_path}/ws`.

### Server-Side Upgrade (Backend)
The Tornado server must handle the upgrade request at the `/ws` path relative to its root.

**Endpoint**: `/ws`
**Protocol**: WebSocket RFC 6455

## Message Integrity
This feature does not introduce new message types, but ensures that existing message flow (training updates, map data) remains stable across the new responsive layout and proxy configurations.

## Failure Modes
- **Subpath Mismatch**: If the proxy rewrites paths incorrectly, the WebSocket handshake will fail (404). The client should attempt to reconnect with an exponential backoff.
- **Protocol Mismatch**: If `https` is used but `ws:` is attempted, browsers will block the connection (Mixed Content error). The resolution algorithm MUST prioritize matching the page protocol.
