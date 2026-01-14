# Walkthrough: Ambush Combat Integration

**Date**: 2026-01-14
**Feature**: Integrated `CombatEncounter` into the Heywood Ambush scene with asynchronous support and refined UX.

## Changes
- **Refactored `CombatEncounter`**: Converted from `cmd.Cmd` to `AsyncCmd`.
- **Ambush Logic**: Updated `HeywoodAmbush` to spawn enemies and trigger combat.
- **UX Improvements**:
    - **Tab Completion**:
        - Fixed `AsyncCmd.py` to auto-register active shell for `prompt_toolkit` routing.
        - Implemented `complete_shoot` to complete enemy names (e.g., "shoot Dirty...").
    - **Stability**: Fixed `do_quit` server crash and scene start regression.
    - **Commands**: Added `take` (equip), `look` (status), `help` (context).

## Verification
### Automated Tests
- `tests/test_ambush_combat_flow.py`: Verifies `CombatEncounter` flow, commands, safe quit, correct `readline` binding, and target completion.
- **Pass Status**: PASS.

### Manual Verification
1. **Trigger Ambush**: Answer phone -> Go to Alley -> Talk to Lenard.
2. **Combat Start**: Verify `COMBAT >` prompt.
3. **Completion**:
    - Type `shoot ` and press Tab. Verify you see "Dirty Cop 1", "Dirty Cop 2", etc.
    - Type `shoot Dirty` and Tab. Verify it auto-completes.
4. **Commands**: Test `look`, `shoot <handle>`, `take`, `quit`.

## Artifacts
- `NeonCore/game_mechanics/combat_system.py`
- `NeonCore/core/async_cmd.py`
- `tests/test_ambush_combat_flow.py`
