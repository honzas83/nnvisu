# Data Model: Usability Layout Refactor

## UI Components (Logical Entities)

### 1. Training Data Panel
Container for data-related tools.
- **Palette**: Swatch selection.
- **Eraser**: Tool toggle.
- **Clear Data**: Action button.

### 2. Training & History Panel
Container for model execution and review.
- **Play/Pause**: Primary control.
- **Architecture Input**: Configuration field.
- **Reset**: Action button.
- **History Control Group**: Combined seekbar and status metrics.

## State Management (Frontend)
No new state variables are introduced. The refactor focuses on the visual mapping of existing state:
- `isTraining` -> Toggles Play/Pause icon/text.
- `currentEpoch`, `currentLoss` -> Displayed in the History Control Group.
- `history` -> Drives the seekbar range and preview.
