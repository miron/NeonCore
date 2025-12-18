import sys
import os
import random
from unittest.mock import MagicMock

# Add project root to path
import importlib.util

# Load module directly to avoid circular imports in package init
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "NeonCore/game_mechanics/combat_shells.py"))
spec = importlib.util.spec_from_file_location("combat_shells", file_path)
combat_shells = importlib.util.module_from_spec(spec)
spec.loader.exec_module(combat_shells)
BrawlingShell = combat_shells.BrawlingShell

def test_brawling_attack():
    print("\n--- Testing Brawling Attack ---")
    
    # Mock Player
    player = MagicMock()
    player.handle = "Player"
    # Mock roll_check to simulate hits and misses
    # First call: Success, Second call: Failure
    player.roll_check.side_effect = [
        {"result": "success", "att_total": 20, "def_total": 10},
        {"result": "failure", "att_total": 10, "def_total": 20}
    ]
    
    # Mock Target
    target = MagicMock()
    target.handle = "Enemy"
    target.take_damage = MagicMock()
    
    # Initialize Shell
    shell = BrawlingShell(player, target)
    
    # Execute Attack
    print("Executing 'attack' command...")
    shell.do_attack("")
    
    # Verify Player Calls
    print("\nVerifying Player Calls:")
    # Should call roll_check twice (ROF 2)
    assert player.roll_check.call_count == 2
    print(" - Player rolled check twice: PASS")
    
    # Verify Target Calls
    print("\nVerifying Target Calls:")
    # Should call take_damage once (because we mocked one hit, one miss)
    assert target.take_damage.call_count == 1
    print(" - Target took damage once: PASS")
    
    # Check damage range (1-6)
    args, kwargs = target.take_damage.call_args
    damage = args[0]
    ignore_armor = kwargs.get('ignore_armor', False)
    
    if 1 <= damage <= 6:
        print(f" - Damage {damage} is within 1d6 range: PASS")
    else:
        print(f" - Damage {damage} is OUT of range: FAIL")
        
    if not ignore_armor:
         print(" - ignore_armor is False: PASS")
    else:
         print(" - ignore_armor is True: FAIL")

if __name__ == "__main__":
    test_brawling_attack()
