# Walkthrough: Ambush Logic & UX Fixes
**Date**: 2026-01-14
**Goal**: Resolve regressions in `HeywoodAmbush` and core UX issues causing player confusion.

## 1. Fixed Missing NPC (Lenard)
**Issue**: Lenard was invisible when entering `heywood_alley` because `do_look` ran *before* the story spawned him.
**Fix**:
- Linked `ActionManager` -> `StoryManager` -> `World` order.
- Modified `HeywoodAmbush.start()` to set location immediately.
- Modified `ActionManager.do_go()` to call `story_manager.update()` *before* looking.

## 2. Fixed Scene Output Order
**Issue**: The "[SCENE START]" text appeared *before* the room description, breaking immersion.
**Fix**:
- Implemented `scene_triggered` flag in `StoryManager`.
- `HeywoodAmbush` now manually calls `world.do_look()` *before* printing scene text.
- `ActionManager` checks `scene_triggered` and skips its default look to prevent duplicates.
**Result**:
1. Room Description (With Visible Characters)
2. Scene Dialogue

## 3. Fixed Empty Input Teleport
**Issue**: Pressing `Enter` repeated the last command (`go north`), causing players to accidentally walk past the ambush scene instandly.
**Fix**:
- Overrode `AsyncCmd.emptyline()` in `ActionManager` to do nothing.

## Verification
### To Reproduce Success:
1. Start Game.
2. `phone call`.
3. `answer`.
4. `go north` (to Industrial Park).
5. `go north` (to Alley).
6. **Verify Output**:
   - Room Description shows "Visible Characters: Lenard".
   - Scene Text appears *below* Room Description.
7. **Verify Input**:
   - Press `Enter`.
   - **Result**: Nothing happens (Prompt refreshes). You are NOT moved to the Warehouse.

## Artifacts Updated
- `NeonCore/story_modules/heywood_ambush.py`
- `NeonCore/managers/action_manager.py`
- `NeonCore/managers/story_manager.py`
- `tests/test_ambush_logic.py`
