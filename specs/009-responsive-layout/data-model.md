# Data Model: Responsive Layout & Metadata

## Entities

### ProjectMetadata
Represents the core identity and environment configuration of the application.

| Field | Type | Description |
|-------|------|-------------|
| author | String | "Jan Švec <honzas@kky.zcu.cz>" |
| version | String | "1.0" |
| environment | String | "CPU-only" |
| repo_url | String | "https://github.com/honzas83/nnvisu" |

### LayoutConfiguration
Defines the responsive behavior of the frontend.

| Field | Type | Description |
|-------|------|-------------|
| breakpoint | Number | 1024 (pixels) |
| sidebar_width | Number | 400 (pixels) |
| stack_order_narrow | String | "Controls-Top" (Controls then Canvas) |
| canvas_behavior_narrow | String | "Scale-to-fit" (Maintain aspect ratio) |

## State Transitions

### Layout Switching
1. **Trigger**: Viewport resize event or initial load.
2. **Condition**: `window.innerWidth >= 1024`.
3. **Action**: 
   - Apply `display: grid` to `#app`.
   - Set controls/header to `grid-area: sidebar`.
   - Set canvas to `grid-area: main`.
   - Enable independent vertical scroll on `sidebar`.
4. **Alternative**: If `window.innerWidth < 1024`, revert to single column (flex-direction: column).
