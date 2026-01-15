import unittest
from unittest.mock import MagicMock, AsyncMock
from NeonCore.game_mechanics.combat_system import CombatEncounter

class TestCombatCompletion(unittest.TestCase):
    def test_complete_take(self):
        # Setup
        mock_player = MagicMock()
        mock_player.inventory = ["Heavy Pistol", "Medkit"]
        mock_io = AsyncMock()
        
        combat = CombatEncounter(mock_player, [], mock_io)
        
        # Test 1: Complete 'Heavy'
        results = combat.complete_take("Heavy", "take Heavy", 0, 0)
        self.assertIn("Heavy Pistol ", results)
        
        # Test 2: Case Insensitive
        results = combat.complete_take("med", "take med", 0, 0)
        self.assertIn("Medkit ", results)

if __name__ == '__main__':
    unittest.main()
