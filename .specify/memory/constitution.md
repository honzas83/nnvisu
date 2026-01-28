<!--
SYNC IMPACT REPORT
Version: 0.0.0 -> 1.0.0
Changes:
- Established initial constitution for 'nnvisu'.
- Defined 4 core principles: Code Quality, Realtime Architecture, Testing, UX.
- Added Performance & Limits section.
- Added Development Workflow section.
Templates:
- .specify/templates/plan-template.md: ✅ Compatible
- .specify/templates/spec-template.md: ✅ Compatible
- .specify/templates/tasks-template.md: ✅ Compatible
-->

# nnvisu Constitution

## Core Principles

### I. High Assurance Code Quality
Code must be statically verifiable and idiomatic Python. We enforce **strict typing** via **Mypy** and rigorous linting/formatting via **Ruff**. Zero tolerance for warnings in CI. Type hints are mandatory for all function signatures to ensure long-term maintainability and correctness.

### II. Realtime-First Architecture
The system relies on **Tornado** and **Websockets** for low-latency, bidirectional communication. Blocking operations in the main event loop are strictly prohibited to ensure high concurrency. All I/O must be asynchronous to maintain performance under load.

### III. Rigorous Testing Standards
Testing is not an afterthought; it defines the feature. We follow a test-first approach where applicable. Unit tests verify business logic, while integration tests ensure the Tornado/Websocket layer functions correctly. Flaky tests are treated as critical failures and must be resolved immediately.

### IV. User Experience Consistency
Interfaces must be predictable, responsive, and uniform. Realtime state changes should be reflected immediately to the user. Visual components and interaction patterns must remain consistent across the application to reduce cognitive load.

## Performance & Limits

*   **Latency Targets**: Websocket message handling should aim for <50ms processing time to ensure a "realtime" feel.
*   **Concurrency**: The architecture must support multiple concurrent websocket connections without significant degradation.
*   **Resource Management**: Async tasks must be properly managed and cleaned up to prevent memory leaks. Event loops must remain unblocked.

## Development Workflow

1.  **Static Analysis**: Run `ruff check .` and `mypy .` before every commit. Clean output is required.
2.  **Verification**: Run `pytest` (or equivalent) to ensure no regressions and that new features meet requirements.
3.  **Code Review**: PRs must verify compliance with these principles. Complexity must be justified.

## Governance

*   **Supremacy**: This constitution supersedes all other technical practices or verbal agreements.
*   **Amendments**: Changes to these principles require documentation, justification, and team consensus.
*   **Compliance**: Temporary deviations (e.g., during rapid prototyping) must be explicitly marked with `TODO(refactor)` and resolved before merging to the main branch.

**Version**: 1.0.0 | **Ratified**: 2026-01-28 | **Last Amended**: 2026-01-28