# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

The current system relies on a client-driven "stateless" loop where the client sends data+model, the server trains one step, and replies. This causes massive network overhead and blocks the server.

**Core Changes:**
1.  **Stateful Backend**: Introduce `TrainingSession` to hold `Model`, `Data`, and `Trainer` instance per connection.
2.  **Background Thread**: Run the training loop in a dedicated thread.
3.  **Producer-Consumer Pattern**: Training thread updates model (Producer). Main loop samples model, generates map, and sends updates (Consumer).
4.  **Binary Protocol**: Optimize heavy visualization data (classification map) to raw binary.

## Constitution Check

- **Code Quality**: Will use `threading` and proper typing.
- **Realtime Architecture**: Decoupling ensures the main loop is never blocked by training.
- **Performance**: Binary protocol and frame dropping explicitly address performance limits.

## Phase 0: Outline & Research

- [x] Research decoupling strategies (Threads vs Async).
- [x] Define binary protocol format.
- [x] Identify state management needs (Moving from Stateless to Stateful).

## Phase 1: Design & Contracts

- [ ] Create `data-model.md` to define `TrainingSession` and new binary message formats.
- [ ] Create `contracts/binary_protocol.md` for the new websocket protocol.
- [ ] Create `quickstart.md` updating instructions for the new flow.
- [ ] Update agent context.

## Phase 2: Implementation (Planned)

### Backend Refactor
1.  Create `TrainingSession` class in `logic/session.py`.
2.  Implement `ThreadedTrainer` wrapper in `logic/trainer.py`.
3.  Update `handlers.py` to manage sessions and handle `start/stop` commands.

### Protocol Optimization
1.  Implement binary serialization for classification maps.
2.  Update `handlers.py` to send binary frames.

### Frontend Adaptation
1.  Update `state_manager.js` to handle binary messages.
2.  Refactor `main.js` to send `start` command instead of driving the loop.

## Phase 3: Verification

1.  Unit test `TrainingSession` thread safety.
2.  Integration test with network throttling (using `tc` or browser simulation).

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
