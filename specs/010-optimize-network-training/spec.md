# Feature Specification: Optimize Network Training

**Feature Branch**: `010-optimize-network-training`
**Created**: 2026-02-03
**Status**: Draft
**Input**: User description: "If deployed over the slower network, the training is rapidly slower. Propose valid solutions."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decoupled Training Performance (Priority: P1)

As a Researcher, I want the neural network training to proceed at its maximum possible speed regardless of the network connection quality to the visualization client, so that my experiments are not delayed by visualization overhead.

**Why this priority**: Core issue reported. Training speed should be compute-bound, not I/O-bound.

**Independent Test**: Run training with a network throttler (e.g., `tc` or browser devtools) limiting bandwidth to 500kbps. Compare training iterations per second against a baseline with no network limit.

**Acceptance Scenarios**:

1. **Given** a training session is active, **When** the network bandwidth drops significantly (e.g., < 1Mbps), **Then** the backend training loop continues to execute at >90% of its normal speed.
2. **Given** a slow network connection, **When** the visualization client connects, **Then** the training speed does not degrade.

---

### User Story 2 - Adaptive Visualization Updates (Priority: P2)

As a Researcher, I want the visualization to update as frequently as the network allows without building up a backlog, so that I see the most current state of the model rather than delayed historical data.

**Why this priority**: Ensures the visualization remains useful and "live" even if it skips frames.

**Independent Test**: Connect via a high-latency link. Observe that the displayed step number increases in jumps (skipping intermediate steps) rather than lagging behind the actual backend step.

**Acceptance Scenarios**:

1. **Given** the training is running faster than the network can transmit updates, **When** a new update is sent, **Then** it represents the most recent training state, dropping intermediate states if necessary.
2. **Given** a network backlog, **When** the queue size exceeds a threshold, **Then** the system drops older packets to recover real-time latency.

---

### Edge Cases

- **Network Disconnection**: The training should continue uninterrupted if the client disconnects completely.
- **Extremely Low Bandwidth**: If bandwidth is insufficient for even minimal updates, the system should prioritize keep-alive/status messages over heavy weight visualizations.

## Requirements *(mandatory)*

### Assumptions

- **A-001**: The primary performance bottleneck causing the reported slowness is network throughput or latency, not client-side rendering performance.
- **A-002**: Users prefer a responsive UI and real-time "latest state" visualization over seeing every single intermediate training step.
- **A-003**: The client environment (modern browser) supports efficient parsing of binary data formats (e.g., ArrayBuffer).

### Functional Requirements

- **FR-001**: The system MUST execute the training loop in a non-blocking manner relative to the network I/O (e.g., using separate threads or non-blocking queues).
- **FR-002**: The system MUST implement an update coalescing or frame-dropping mechanism on the server side to handle backpressure when the client cannot consume data fast enough.
- **FR-003**: The system MUST optimize the data payload size for network transmission (e.g., using binary formats or compression instead of verbose text/JSON where appropriate).
- **FR-004**: The system MUST prioritize the latest data state; if the send queue is full, the oldest unsent data (except essential control messages) should be discarded.
- **FR-005**: The frontend MUST handle variable update rates gracefully without visual stuttering in the UI controls (though the data plots may update less frequently).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Training throughput (iterations/second) decreases by less than 10% when network bandwidth is throttled to 1 Mbps compared to localhost speed.
- **SC-002**: Latency between the "current training step" on the backend and the "displayed step" on the frontend remains under 2 seconds, regardless of network speed (by dropping intermediate frames).
- **SC-003**: Payload size per update is reduced by at least 40% compared to the current implementation (if currently using unoptimized JSON).