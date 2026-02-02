# Quickstart: Usability Layout Refactor

## Verification Steps

1. **Start the Application**:
   ```bash
   python -m nnvisu.app
   ```

2. **Verify Layout Grouping**:
   - Check for two panels: "Training Data" and "Training & History".
   - Confirm buttons are correctly placed within these panels.

3. **Verify Header & How-to**:
   - Title should be "nnvisu".
   - Confirm the 4-step "How to use" guide is visible below the header.

4. **Verify Architecture Input**:
   - Label should be "Network Architecture (Hidden Layers)".
   - Confirm example "e.g., 10-5-2" is visible.

5. **Verify Integrated Status**:
   - Start training.
   - Confirm "Epoch" and "Loss" are displayed near the history seekbar.
   - Verify the seekbar width is constrained (not full page width).
