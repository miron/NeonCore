
import unittest
from unittest.mock import MagicMock, AsyncMock
from NeonCore.managers.action_manager import ActionManager

class TestBrawlingRegression(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_deps = MagicMock()
        self.mock_deps.char_mngr = MagicMock()
        self.mock_deps.npc_manager = MagicMock()
        self.mock_deps.world = MagicMock()
        self.mock_deps.story_manager = MagicMock()
        self.mock_deps.story_manager.update = AsyncMock()
        self.mock_deps.cmd_mngr = MagicMock()
        self.mock_deps.skill_check = MagicMock()

        # Initialize ActionManager with mocks
        self.action_manager = ActionManager(self.mock_deps)
        self.action_manager.game_state = "before_perception_check"
        self.action_manager.io = AsyncMock()

    async def test_brawling_sp_field_access(self):
        """Regression Test: Ensure Brawling doesn't crash when accessing NPC armor (SP)"""
        # Setup
        player = MagicMock()
        # Mock roll_check to return success so damage logic runs
        player.roll_check.return_value = {
            "result": "success", 
            "att_total": 20, 
            "def_total": 10,
            "details": {"att_crit": None, "def_crit": None}
        }
        player.stats = {"body": 5} # 1d6 damage
        self.mock_deps.char_mngr.player = player
        
        target_npc = MagicMock()
        target_npc.handle = "Lenard"
        # Mock defence dict properly
        target_npc.defence = {"sp": 7}
        # Simulate take_damage returning 0 (Absorbed)
        target_npc.take_damage.return_value = 0
        
        self.mock_deps.npc_manager.get_npc.return_value = target_npc
        
        # Execute
        try:
            await self.action_manager.do_use_skill("brawling lenard")
        except AttributeError as e:
            self.fail(f"Brawling crashed with AttributeError: {e}")
            
        # Verify
        # Verify we tried to print the absorbed message
        # We can inspect the io calls to ensure the message contains "Absorbed by Armor"
        found = False
        for call in self.action_manager.io.send.call_args_list:
            args, _ = call
            if "Absorbed by Armor" in args[0]:
                found = True
                break
        self.assertTrue(found, "Should report that damage was absorbed by armor")

if __name__ == "__main__":
    unittest.main()
