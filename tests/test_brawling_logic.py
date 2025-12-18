import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to path to ensure imports work correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import importlib.util

# Helper to import module bypassing package __init__ to avoid circular deps
def import_brawling_shell():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../NeonCore/game_mechanics/combat_shells.py"))
    spec = importlib.util.spec_from_file_location("combat_shells", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.BrawlingShell

BrawlingShell = import_brawling_shell()

class TestBrawlingLogic(unittest.TestCase):
    def setUp(self):
        # Mock Player
        self.player = MagicMock()
        self.player.handle = "Player"
        
        # Mock Target
        self.target = MagicMock()
        self.target.handle = "Enemy"
        
        # Initialize Shell
        self.shell = BrawlingShell(self.player, self.target)

    def test_do_attack_mechanics(self):
        """
        Test that do_attack:
        1. Attacks twice (ROF 2).
        2. Rolls 1d6 damage on hit.
        3. Applies damage respecting armor (ignore_armor=False).
        """
        # Mock roll_check to simulate:
        # 1. Success (Hit)
        # 2. Failure (Miss)
        self.player.roll_check.side_effect = [
            {"result": "success", "att_total": 20, "def_total": 10},
            {"result": "failure", "att_total": 10, "def_total": 20}
        ]
        
        # Mock random.randint for damage roll to be deterministic (e.g., 4)
        with patch("random.randint", return_value=4):
            # Execute Attack
            self.shell.do_attack("")
            
        # Verify Player Calls (ROF 2 -> 2 checks)
        self.assertEqual(self.player.roll_check.call_count, 2, "Should perform 2 skill checks (ROF 2)")
        
        # Verify Target Calls
        # Should call take_damage once (only first hit succeeded)
        self.target.take_damage.assert_called_once()
        
        # Verify arguments passed to take_damage
        args, kwargs = self.target.take_damage.call_args
        damage_passed = args[0]
        ignore_armor_passed = kwargs.get('ignore_armor', False)
        
        self.assertEqual(damage_passed, 4, "Damage should be the result of the die roll")
        self.assertFalse(ignore_armor_passed, "Brawling attacks should NOT ignore armor")

if __name__ == "__main__":
    unittest.main()
