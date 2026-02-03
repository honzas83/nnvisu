# Research: Optimize Network Training

## Technical Decisions

### 1. Decoupling Training from Network I/O
**Decision:** Use a background thread (`threading.Thread`) for the training loop and a thread-safe `queue.Queue` (maxsize=1) for communicating updates to the main Tornado event loop.

**Rationale:**
- **Non-blocking:** The training loop (CPU bound) must not block the Tornado I/O loop.
- **Simplicity:** Python threads share memory, making it easy to share the `Model` and `Data` between the training loop and the visualization generator without complex IPC. The GIL is released during PyTorch operations, allowing concurrency.
- **Backpressure Handling:** A queue with `maxsize=1` automatically implements the "latest only" requirement. If the network (consumer) is slow, the queue stays full, and the producer (training thread) can overwrite or skip pushing (if using `put_nowait` with handling) or we just let the consumer pull the latest. Actually, a "LIFO" or "overwrite" queue behavior is best.

**Alternatives Considered:**
- **`multiprocessing`**: Better for CPU isolation, but sharing the large model/data state is expensive (pickling/serialization). Overkill since PyTorch releases GIL.
- **`asyncio` / Coroutines**: Not suitable because the training step itself is synchronous CPU work.

### 2. Update Mechanism & Flow Control
**Decision:** The server will implement a "Training Session" state.
- **Client -> Server**: `start_training`, `stop_training`, `update_config`.
- **Server -> Client**: Periodic `map_update` and `step_result`.
- **Throttling**: The main loop will use a `PeriodicCallback` (e.g., every 33ms for 30fps) to check the queue. If the queue has data, send it. If the network buffer is full (Tornado can check `stream.write_buffer_size`), skip sending to avoid unlimited buffering.

### 3. Binary Data Protocol
**Decision:** Use WebSocket Binary Frames for the `map_update`.
- **Format**: A simple header (1 byte for type) followed by raw RGB bytes.
- **Client**: Parse using `DataView` or `Uint8Array`.

**Rationale:**
- Base64 encoding adds ~33% overhead and requires CPU for encoding/decoding.
- Raw bytes are the most compact representation.

## Unknowns & Risks
- **State Management**: The current `StatelessTrainer` implies no persistence. We need to introduce a persistent `TrainingSession` object per websocket connection to hold the model and data.
- **Concurrency Safety**: Sharing the `model` between the training thread (writing weights) and the visualization thread/callback (reading weights for inference) requires locking (`threading.Lock`) to prevent reading inconsistent states.

## Validated Assumptions
- Tornado allows writing to the websocket from the main thread while a background thread does the work.
- Modern browsers support binary websockets easily.
