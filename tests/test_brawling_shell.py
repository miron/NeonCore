
import unittest
from unittest.mock import MagicMock, AsyncMock, call
import sys
import os
import asyncio

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from NeonCore.game_mechanics.combat_shells import BrawlingShell

class TestBrawlingShell(unittest.IsolatedAsyncioTestCase):
    async def test_attack_flow(self):
        # Mock Player
        player = MagicMock()
        player.handle = "Player"
        # Mock roll_check: 1st hit, 2nd miss
        player.roll_check.side_effect = [
            {"result": "success", "att_total": 20, "def_total": 10},
            {"result": "failure", "att_total": 10, "def_total": 20}
        ]

        # Mock Target
        target = MagicMock()
        target.handle = "Enemy"
        target.take_damage = MagicMock()

        # Mock IO
        mock_io = AsyncMock()

        # Initialize Shell
        shell = BrawlingShell(player, target, mock_io)

        # Execute Attack
        await shell.do_attack("")

        # Verifications
        # 1. Player should roll twice (ROF 2)
        self.assertEqual(player.roll_check.call_count, 2)
        
        # 2. Target should take damage once (only 1 success)
        self.assertEqual(target.take_damage.call_count, 1)
        
        # 3. Check IO calls (Flavor text)
        # Should have sent "You launch a flurry...", "Attack 1", "Damage Roll...", "Attack 2", "MISS!"
        # Just verify call count > 0
        self.assertTrue(mock_io.send.called)

if __name__ == "__main__":
    unittest.main()
